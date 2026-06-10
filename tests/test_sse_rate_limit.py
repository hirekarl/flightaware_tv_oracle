"""Tests for concurrent connection rate limiting on /api/fleet/stream.

These tests FAIL until stream_fleet() enforces a configurable connection cap
via app.state.max_sse_connections / app.state.active_sse_connections.

Expected implementation contract:
- lifespan reads SSE_MAX_CONNECTIONS env var (default >= 1) into
  app.state.max_sse_connections
- lifespan initialises app.state.active_sse_connections = 0
- stream_fleet() returns HTTP 429 + Retry-After header when
  active_sse_connections >= max_sse_connections
- stream_fleet() increments active_sse_connections before streaming
- _sse_fleet_stream() decrements active_sse_connections in a finally block
"""

import asyncio
from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from backend.agents.coordinator import CoordinatorAgent
from backend.main import app
from backend.models.flight import AiAnalysis

_BASE = "http://test"
_STREAM = "/api/fleet/stream"

_MOCK_ANALYSIS = AiAnalysis(
    summaryTitle="Test",
    rootCause="Test cause.",
    downstreamImpact="Test impact.",
    recommendedAction="Test action.",
)


async def _one_shot_stream(coordinator: CoordinatorAgent) -> AsyncGenerator[str, None]:
    """Finite stand-in for _sse_fleet_stream — yields one event then stops."""
    yield "data: []\n\n"


@pytest.fixture(autouse=True)
def sse_state(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Seed app.state, mock coordinator, and replace the infinite SSE generator."""
    mock_coordinator: CoordinatorAgent = AsyncMock(spec=CoordinatorAgent)
    mock_coordinator.analyze.return_value = _MOCK_ANALYSIS  # type: ignore[attr-defined]
    app.state.coordinator = mock_coordinator
    app.state.active_sse_connections = 0
    app.state.max_sse_connections = 10
    # Replace the infinite loop generator with a finite one so tests don't hang.
    monkeypatch.setattr("backend.main._sse_fleet_stream", _one_shot_stream)
    yield
    for attr in ("coordinator", "active_sse_connections", "max_sse_connections"):
        try:
            delattr(app.state, attr)
        except (AttributeError, KeyError):
            pass


async def test_stream_accepted_when_below_limit() -> None:
    """A connection is accepted with 200 when the limit has not been reached."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        async with client.stream("GET", _STREAM) as r:
            assert r.status_code == 200


async def test_stream_content_type_is_event_stream() -> None:
    """Accepted connections must carry text/event-stream content type."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        async with client.stream("GET", _STREAM) as r:
            assert r.status_code == 200
            assert "text/event-stream" in r.headers["content-type"]


async def test_stream_rejected_at_capacity() -> None:
    """A new connection is rejected with 429 when active count equals the limit."""
    app.state.active_sse_connections = app.state.max_sse_connections
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        r = await client.get(_STREAM)
    assert r.status_code == 429


async def test_rejected_response_has_retry_after_header() -> None:
    """429 response must include a Retry-After header."""
    app.state.active_sse_connections = app.state.max_sse_connections
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        r = await client.get(_STREAM)
    assert "retry-after" in r.headers


async def test_retry_after_is_positive_integer() -> None:
    """Retry-After value must be a positive integer (seconds until retry)."""
    app.state.active_sse_connections = app.state.max_sse_connections
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        r = await client.get(_STREAM)
    assert int(r.headers["retry-after"]) > 0


async def test_rejected_response_body_has_detail() -> None:
    """429 response body must be JSON with a 'detail' key."""
    app.state.active_sse_connections = app.state.max_sse_connections
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        r = await client.get(_STREAM)
    assert "detail" in r.json()


async def test_active_count_increments_on_accepted_connection() -> None:
    """active_sse_connections reaches 1 when a connection is accepted.

    ASGITransport runs the full ASGI app inline inside handle_async_request,
    so the counter is incremented AND decremented before the stream context
    yields the response to the caller.  A spy on State.__setattr__ captures
    the peak value instead of reading it mid-stream.
    """
    seen: list[int] = []
    _orig = type(app.state).__setattr__

    def _spy(self: object, name: str, value: object) -> None:
        if name == "active_sse_connections":
            seen.append(value)  # type: ignore[arg-type]
        _orig(self, name, value)  # type: ignore[arg-type]

    type(app.state).__setattr__ = _spy  # type: ignore[method-assign]
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=_BASE
        ) as client:
            async with client.stream("GET", _STREAM) as r:
                assert r.status_code == 200
    finally:
        type(app.state).__setattr__ = _orig  # type: ignore[method-assign]

    assert 1 in seen


async def test_active_count_decrements_after_disconnect() -> None:
    """active_sse_connections returns to 0 after the connection closes."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        async with client.stream("GET", _STREAM) as r:
            assert r.status_code == 200
    await asyncio.sleep(0)
    assert app.state.active_sse_connections == 0


async def test_slot_freed_after_disconnect_allows_new_connection() -> None:
    """A connection that closes frees its slot so the next request is accepted."""
    app.state.max_sse_connections = 1
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        async with client.stream("GET", _STREAM) as r:
            assert r.status_code == 200
    await asyncio.sleep(0)
    async with AsyncClient(transport=ASGITransport(app=app), base_url=_BASE) as client:
        async with client.stream("GET", _STREAM) as r:
            assert r.status_code == 200


async def test_lifespan_sets_default_max_connections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """lifespan must set app.state.max_sse_connections to a positive int."""
    monkeypatch.setattr(
        "backend.main.CoordinatorAgent", lambda: AsyncMock(spec=CoordinatorAgent)
    )
    del app.state.max_sse_connections  # clear the fixture-seeded value
    from backend.main import lifespan

    async with lifespan(app):
        assert isinstance(app.state.max_sse_connections, int)
        assert app.state.max_sse_connections > 0


async def test_lifespan_reads_sse_max_connections_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """lifespan must read SSE_MAX_CONNECTIONS from the environment."""
    monkeypatch.setenv("SSE_MAX_CONNECTIONS", "7")
    monkeypatch.setattr(
        "backend.main.CoordinatorAgent", lambda: AsyncMock(spec=CoordinatorAgent)
    )
    from backend.main import lifespan

    async with lifespan(app):
        assert app.state.max_sse_connections == 7
