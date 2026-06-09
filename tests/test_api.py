"""Integration tests for FastAPI endpoints — HTTP contract and SSE event format."""

import json
from collections.abc import Generator
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.responses import StreamingResponse

from backend.agents.coordinator import CoordinatorAgent
from backend.main import _sse_fleet_stream, app, stream_fleet
from backend.models.flight import AiAnalysis, FlightState

_MOCK_FLEET_IDS = {"AA123", "UA456", "DL789", "SW202"}


def _stub_analysis() -> AiAnalysis:
    return AiAnalysis(
        summaryTitle="Stub",
        rootCause="Stub root cause.",
        downstreamImpact="Stub downstream impact.",
        recommendedAction="Stub action.",
    )


@pytest.fixture(autouse=True)
def seed_coordinator() -> Generator[None, None, None]:
    """Seed app.state.coordinator with a mock for every test in this module."""
    mock: CoordinatorAgent = AsyncMock(spec=CoordinatorAgent)
    mock.analyze.return_value = _stub_analysis()  # type: ignore[attr-defined]
    app.state.coordinator = mock
    yield
    try:
        delattr(app.state, "coordinator")
    except (AttributeError, KeyError):
        pass


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------


async def test_health_returns_200() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.status_code == 200


async def test_health_body_is_ok() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# /api/fleet  (snapshot)
# ---------------------------------------------------------------------------


async def test_fleet_snapshot_returns_200() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/fleet")
    assert response.status_code == 200


async def test_fleet_snapshot_is_list() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/fleet")
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) > 0


async def test_fleet_snapshot_items_validate_as_flight_states() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/fleet")
    for item in response.json():
        FlightState(**item)


# ---------------------------------------------------------------------------
# /api/fleet/stream — response object (inspect directly; avoids consuming
# the infinite SSE generator via the transport layer)
# ---------------------------------------------------------------------------


async def test_stream_returns_streaming_response() -> None:
    response = await stream_fleet()
    assert isinstance(response, StreamingResponse)


async def test_stream_media_type() -> None:
    response = await stream_fleet()
    assert response.media_type == "text/event-stream"


async def test_stream_cache_control_header() -> None:
    response = await stream_fleet()
    assert response.headers["cache-control"] == "no-cache"


async def test_stream_x_accel_buffering_header() -> None:
    response = await stream_fleet()
    assert response.headers["x-accel-buffering"] == "no"


# ---------------------------------------------------------------------------
# _sse_fleet_stream() — SSE event format and payload schema
# (call the generator directly with a mock coordinator)
# ---------------------------------------------------------------------------


@pytest.fixture
async def first_sse_event() -> str:
    """Return the first raw SSE event from the generator."""
    mock: CoordinatorAgent = AsyncMock(spec=CoordinatorAgent)
    mock.analyze.return_value = _stub_analysis()  # type: ignore[attr-defined]
    gen = _sse_fleet_stream(mock)
    try:
        return await gen.__anext__()
    finally:
        await gen.aclose()


async def test_sse_event_starts_with_data_prefix(first_sse_event: str) -> None:
    assert first_sse_event.startswith("data: ")


async def test_sse_event_ends_with_double_newline(first_sse_event: str) -> None:
    assert first_sse_event.endswith("\n\n")


async def test_sse_payload_is_nonempty_list(first_sse_event: str) -> None:
    payload = json.loads(first_sse_event[len("data: ") :].strip())
    assert isinstance(payload, list)
    assert len(payload) > 0


async def test_sse_payload_items_validate_as_flight_states(
    first_sse_event: str,
) -> None:
    payload = json.loads(first_sse_event[len("data: ") :].strip())
    for item in payload:
        FlightState(**item)


async def test_sse_payload_contains_all_flights(first_sse_event: str) -> None:
    payload = json.loads(first_sse_event[len("data: ") :].strip())
    assert {item["flightId"] for item in payload} == _MOCK_FLEET_IDS
