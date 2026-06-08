"""Integration tests for FastAPI endpoints — HTTP contract and SSE event format."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi.responses import StreamingResponse

from backend.main import _enrich_flight, _sse_fleet_stream, app, stream_fleet
from backend.models.flight import (
    AiAnalysis,
    DeviationType,
    FlightState,
    OperationalStatus,
    Route,
    Telemetry,
)

_MOCK_FLEET_IDS = {"AA123", "UA456", "DL789", "SW202"}


def _stub_analysis() -> AiAnalysis:
    return AiAnalysis(
        summaryTitle="Stub",
        rootCause="Stub root cause.",
        downstreamImpact="Stub downstream impact.",
        recommendedAction="Stub action.",
    )


def _mock_coordinator() -> MagicMock:
    mock = MagicMock()
    mock.analyze = AsyncMock(return_value=_stub_analysis())
    return mock


def _flight(status: OperationalStatus = OperationalStatus.NORMAL) -> FlightState:
    return FlightState(
        flightId="TS001",
        aircraftType="B738",
        route=Route(departure="KJFK", destination="KORD"),
        operationalStatus=status,
        deviationType=DeviationType.NONE,
        telemetry=Telemetry(fuelRemainingMin=120, altitude=35000),
        aiAnalysis=AiAnalysis(
            summaryTitle="Test",
            rootCause=".",
            downstreamImpact=".",
            recommendedAction=".",
        ),
    )


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
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


async def test_fleet_snapshot_items_validate_as_flight_states() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/fleet")
    for item in response.json():
        FlightState(**item)


# ---------------------------------------------------------------------------
# /api/fleet/stream — response headers (inspect StreamingResponse directly;
# httpx ASGI transport deadlocks on infinite SSE generators)
# ---------------------------------------------------------------------------


async def test_stream_returns_streaming_response() -> None:
    with patch("backend.main.CoordinatorAgent"):
        response = await stream_fleet()
    assert isinstance(response, StreamingResponse)


async def test_stream_media_type() -> None:
    with patch("backend.main.CoordinatorAgent"):
        response = await stream_fleet()
    assert response.media_type == "text/event-stream"


async def test_stream_cache_control_header() -> None:
    with patch("backend.main.CoordinatorAgent"):
        response = await stream_fleet()
    assert response.headers["cache-control"] == "no-cache"


async def test_stream_x_accel_buffering_header() -> None:
    with patch("backend.main.CoordinatorAgent"):
        response = await stream_fleet()
    assert response.headers["x-accel-buffering"] == "no"


# ---------------------------------------------------------------------------
# _sse_fleet_stream() — SSE event format and payload schema
# (call the generator directly; avoids infinite-stream ASGI transport issues)
# ---------------------------------------------------------------------------


@pytest.fixture
async def first_sse_event() -> str:
    """Return the first raw SSE line from the generator with a mocked coordinator."""
    with patch("backend.main.CoordinatorAgent") as MockClass:
        MockClass.return_value = _mock_coordinator()
        gen = _sse_fleet_stream()
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


# ---------------------------------------------------------------------------
# _enrich_flight() — NORMAL bypass and AI enrichment
# ---------------------------------------------------------------------------


async def test_normal_flight_bypasses_coordinator() -> None:
    coord = _mock_coordinator()
    await _enrich_flight(coord, _flight(OperationalStatus.NORMAL))
    coord.analyze.assert_not_called()


async def test_normal_flight_returned_unchanged() -> None:
    flight = _flight(OperationalStatus.NORMAL)
    coord = _mock_coordinator()
    result = await _enrich_flight(coord, flight)
    assert result is flight


async def test_critical_flight_calls_coordinator() -> None:
    coord = _mock_coordinator()
    flight = _flight(OperationalStatus.CRITICAL)
    await _enrich_flight(coord, flight)
    coord.analyze.assert_called_once_with(flight)


async def test_enriched_flight_carries_ai_analysis() -> None:
    coord = _mock_coordinator()
    result = await _enrich_flight(coord, _flight(OperationalStatus.WARNING))
    assert result.aiAnalysis.summaryTitle == "Stub"
