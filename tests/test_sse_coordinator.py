"""Tests for CoordinatorAgent wiring into the /api/fleet/stream SSE endpoint.

These tests target the *generator function* directly rather than through HTTP to
avoid the hang that results from the 5-second sleep blocking connection cleanup.

Assumed implementation signature:
    async def _sse_fleet_stream(
        coordinator: CoordinatorAgent,
    ) -> AsyncGenerator[str, None]

These tests FAIL until the SSE generator is updated to accept and call a coordinator.
"""

import json
from unittest.mock import AsyncMock

import pytest

from backend.agents.coordinator import CoordinatorAgent
from backend.main import _sse_fleet_stream
from backend.models.flight import AiAnalysis, FlightState

_COORDINATOR_ANALYSIS = AiAnalysis(
    summaryTitle="Coordinator-Generated Title",
    rootCause="Coordinator root cause.",
    downstreamImpact="Coordinator downstream impact.",
    recommendedAction="Coordinator recommended action.",
)


@pytest.fixture
def mock_coordinator() -> CoordinatorAgent:
    coordinator: CoordinatorAgent = AsyncMock(spec=CoordinatorAgent)
    coordinator.analyze.return_value = _COORDINATOR_ANALYSIS  # type: ignore[attr-defined]
    return coordinator


async def _first_event(coordinator: CoordinatorAgent) -> list[dict]:
    """Consume one SSE event from the generator and immediately close it."""
    gen = _sse_fleet_stream(coordinator)
    try:
        raw = await gen.__anext__()
    finally:
        await gen.aclose()
    assert raw.startswith("data: "), f"Expected SSE data line, got: {raw!r}"
    return json.loads(raw[len("data: ") :].strip())


async def test_sse_generator_event_has_correct_sse_format(
    mock_coordinator: CoordinatorAgent,
) -> None:
    gen = _sse_fleet_stream(mock_coordinator)
    try:
        raw = await gen.__anext__()
    finally:
        await gen.aclose()
    assert raw.startswith("data: ")
    assert raw.endswith("\n\n")


async def test_sse_generator_uses_coordinator_analysis_not_static_mock(
    mock_coordinator: CoordinatorAgent,
) -> None:
    """aiAnalysis must come from coordinator.analyze(), not static simulation data."""
    payload = await _first_event(mock_coordinator)
    for flight_data in payload:
        assert (
            flight_data["aiAnalysis"]["summaryTitle"] == "Coordinator-Generated Title"
        ), (
            f"Flight {flight_data['flightId']} carries static mock aiAnalysis. "
            "Wire coordinator.analyze() into _sse_fleet_stream."
        )


async def test_sse_generator_calls_coordinator_once_per_flight(
    mock_coordinator: CoordinatorAgent,
) -> None:
    payload = await _first_event(mock_coordinator)
    expected = len(payload)
    actual = mock_coordinator.analyze.call_count  # type: ignore[attr-defined]
    assert actual == expected, (
        f"Expected coordinator.analyze() called {expected} times "
        f"(once per flight), got {actual}."
    )


async def test_sse_generator_passes_typed_flight_state_to_coordinator(
    mock_coordinator: CoordinatorAgent,
) -> None:
    """coordinator.analyze() must receive FlightState instances — never raw dicts."""
    await _first_event(mock_coordinator)
    for call in mock_coordinator.analyze.call_args_list:  # type: ignore[attr-defined]
        arg = call.args[0] if call.args else call.kwargs.get("flight")
        assert isinstance(
            arg, FlightState
        ), f"analyze() got {type(arg).__name__}, expected FlightState."


async def test_sse_generator_payload_validates_as_fleet_state_list(
    mock_coordinator: CoordinatorAgent,
) -> None:
    payload = await _first_event(mock_coordinator)
    assert len(payload) > 0
    fleet = [FlightState.model_validate(f) for f in payload]
    assert all(isinstance(f, FlightState) for f in fleet)
