"""Tests for CrewLogisticsAgent.assess() return shape and behavior."""

import pytest

from backend.agents.crew_logistics import (
    _FUEL_CRITICAL_THRESHOLD,
    CrewLogisticsAgent,
)
from backend.models.flight import (
    AiAnalysis,
    DeviationType,
    FlightState,
    OperationalStatus,
    Route,
    Telemetry,
)


def _make_flight(**overrides: object) -> FlightState:
    defaults: dict[str, object] = {
        "flightId": "AA123",
        "aircraftType": "B738",
        "route": Route(departure="KJFK", destination="KORD"),
        "operationalStatus": OperationalStatus.CRITICAL,
        "deviationType": DeviationType.GO_AROUND,
        "telemetry": Telemetry(fuelRemainingMin=45, altitude=2400),
        "aiAnalysis": AiAnalysis(
            summaryTitle="Test",
            rootCause="Root.",
            downstreamImpact="Impact.",
            recommendedAction="Act.",
        ),
    }
    return FlightState(**{**defaults, **overrides})


@pytest.fixture
def agent() -> CrewLogisticsAgent:
    return CrewLogisticsAgent()


async def test_assess_returns_impact_key_for_all_statuses(
    agent: CrewLogisticsAgent,
) -> None:
    for status in OperationalStatus:
        result = await agent.assess(_make_flight(operationalStatus=status))
        assert "impact" in result, f"Expected 'impact' key for status {status}"


async def test_assess_impact_is_non_empty_string_for_all_statuses(
    agent: CrewLogisticsAgent,
) -> None:
    for status in OperationalStatus:
        result = await agent.assess(_make_flight(operationalStatus=status))
        assert isinstance(result["impact"], str) and result["impact"], (
            f"Expected non-empty string for status {status}"
        )


async def test_assess_critical_low_fuel_reports_fuel_critical(
    agent: CrewLogisticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.CRITICAL,
        telemetry=Telemetry(
            fuelRemainingMin=_FUEL_CRITICAL_THRESHOLD - 1, altitude=2400
        ),
    )
    result = await agent.assess(flight)
    assert "Fuel critical" in result["impact"]


async def test_assess_critical_low_fuel_includes_fuel_remaining_minutes(
    agent: CrewLogisticsAgent,
) -> None:
    fuel = _FUEL_CRITICAL_THRESHOLD - 1
    flight = _make_flight(
        operationalStatus=OperationalStatus.CRITICAL,
        telemetry=Telemetry(fuelRemainingMin=fuel, altitude=2400),
    )
    result = await agent.assess(flight)
    assert str(fuel) in result["impact"]


async def test_assess_critical_low_fuel_reports_gate_conflict(
    agent: CrewLogisticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.CRITICAL,
        telemetry=Telemetry(
            fuelRemainingMin=_FUEL_CRITICAL_THRESHOLD - 1, altitude=2400
        ),
    )
    result = await agent.assess(flight)
    assert "Gate conflict" in result["impact"]


async def test_assess_warning_mentions_crew_duty(
    agent: CrewLogisticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.WARNING,
        telemetry=Telemetry(fuelRemainingMin=90, altitude=8000),
    )
    result = await agent.assess(flight)
    assert "crew duty" in result["impact"].lower()


async def test_assess_warning_mentions_downstream_connections(
    agent: CrewLogisticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.WARNING,
        telemetry=Telemetry(fuelRemainingMin=90, altitude=8000),
    )
    result = await agent.assess(flight)
    assert "connections" in result["impact"].lower()


async def test_assess_normal_returns_no_constraints_message(
    agent: CrewLogisticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.NORMAL,
        telemetry=Telemetry(fuelRemainingMin=180, altitude=35000),
    )
    result = await agent.assess(flight)
    assert result["impact"] == "No crew or gate constraints detected."
