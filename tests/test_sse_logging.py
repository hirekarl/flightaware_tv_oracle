"""Tests for structured logging emitted by _sse_fleet_stream per cycle.

Each SSE cycle must emit exactly one INFO record on the "backend.main" logger
containing cycle-level metrics and per-flight forecast vs. actual comparison.

Forecast = the static mock aiAnalysis.summaryTitle from generate_mock_fleet().
Actual   = the aiAnalysis.summaryTitle returned by coordinator.analyze().
"""

import logging
from unittest.mock import AsyncMock

import pytest

from backend.agents.coordinator import CoordinatorAgent
from backend.main import _sse_fleet_stream
from backend.models.flight import AiAnalysis

_COORDINATOR_TITLE = "Coordinator Title"
_AI_ANALYSIS = AiAnalysis(
    summaryTitle=_COORDINATOR_TITLE,
    rootCause="Coordinator cause.",
    downstreamImpact="Coordinator impact.",
    recommendedAction="Coordinator action.",
)
_LOGGER = "backend.main"
_MOCK_FLEET_SIZE = 4  # generate_mock_fleet() always returns 4 flights


@pytest.fixture
def mock_coordinator() -> CoordinatorAgent:
    coordinator: CoordinatorAgent = AsyncMock(spec=CoordinatorAgent)
    coordinator.analyze.return_value = _AI_ANALYSIS  # type: ignore[attr-defined]
    return coordinator


async def _cycle_records(
    coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> list[logging.LogRecord]:
    """Run one SSE cycle and return log records emitted by backend.main."""
    with caplog.at_level(logging.INFO, logger=_LOGGER):
        gen = _sse_fleet_stream(coordinator)
        try:
            await gen.__anext__()
        finally:
            await gen.aclose()
    return [r for r in caplog.records if r.name == _LOGGER]


async def test_sse_cycle_emits_exactly_one_log_record(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    records = await _cycle_records(mock_coordinator, caplog)
    assert len(records) == 1


async def test_sse_cycle_log_level_is_info(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    records = await _cycle_records(mock_coordinator, caplog)
    assert records[0].levelno == logging.INFO


async def test_sse_cycle_log_fleet_size_equals_generated_fleet(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    records = await _cycle_records(mock_coordinator, caplog)
    assert records[0].fleet_size == _MOCK_FLEET_SIZE  # type: ignore[attr-defined]


async def test_sse_cycle_log_elapsed_ms_is_positive(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    records = await _cycle_records(mock_coordinator, caplog)
    assert records[0].elapsed_ms >= 0  # type: ignore[attr-defined]


async def test_sse_cycle_log_elapsed_ms_is_float(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    records = await _cycle_records(mock_coordinator, caplog)
    assert isinstance(records[0].elapsed_ms, float)  # type: ignore[attr-defined]


async def test_sse_cycle_log_flights_count_matches_fleet_size(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    records = await _cycle_records(mock_coordinator, caplog)
    record = records[0]
    assert len(record.flights) == record.fleet_size  # type: ignore[attr-defined]


async def test_sse_cycle_per_flight_entry_has_flight_id(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    records = await _cycle_records(mock_coordinator, caplog)
    for entry in records[0].flights:  # type: ignore[attr-defined]
        assert "flight_id" in entry
        assert isinstance(entry["flight_id"], str) and entry["flight_id"]


async def test_sse_cycle_per_flight_entry_has_valid_status(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    valid_statuses = {"NORMAL", "WARNING", "CRITICAL"}
    records = await _cycle_records(mock_coordinator, caplog)
    for entry in records[0].flights:  # type: ignore[attr-defined]
        assert entry["status"] in valid_statuses


async def test_sse_cycle_per_flight_forecast_title_is_from_mock_fleet(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """forecast_title must be the original mock aiAnalysis, not coordinator output."""
    records = await _cycle_records(mock_coordinator, caplog)
    for entry in records[0].flights:  # type: ignore[attr-defined]
        assert entry["forecast_title"] != _COORDINATOR_TITLE, (
            "forecast_title must be the original simulation title, not the AI output."
        )


async def test_sse_cycle_per_flight_actual_title_matches_coordinator_output(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """actual_title must be whatever coordinator.analyze() returned."""
    records = await _cycle_records(mock_coordinator, caplog)
    for entry in records[0].flights:  # type: ignore[attr-defined]
        assert entry["actual_title"] == _COORDINATOR_TITLE


async def test_sse_cycle_all_known_flight_ids_appear_in_log(
    mock_coordinator: CoordinatorAgent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Every flight from generate_mock_fleet() must appear in the log."""
    expected_ids = {"AA123", "UA456", "DL789", "SW202"}
    records = await _cycle_records(mock_coordinator, caplog)
    logged_ids = {entry["flight_id"] for entry in records[0].flights}  # type: ignore[attr-defined]
    assert logged_ids == expected_ids
