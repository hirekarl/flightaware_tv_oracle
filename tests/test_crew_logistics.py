"""Tests for CrewLogisticsAgent.assess() return shape and risk logic."""

import pytest

from backend.agents.crew_logistics import _FUEL_CRITICAL_THRESHOLD, CrewLogisticsAgent
from backend.models.flight import (
    AiAnalysis,
    DeviationType,
    FlightState,
    OperationalStatus,
    Route,
    Telemetry,
)


def _flight(
    status: OperationalStatus = OperationalStatus.NORMAL,
    fuel: int = 120,
) -> FlightState:
    return FlightState(
        flightId="TS001",
        aircraftType="B738",
        route=Route(departure="KJFK", destination="KORD"),
        operationalStatus=status,
        deviationType=DeviationType.NONE,
        telemetry=Telemetry(fuelRemainingMin=fuel, altitude=10000),
        aiAnalysis=AiAnalysis(
            summaryTitle="Test",
            rootCause=".",
            downstreamImpact=".",
            recommendedAction=".",
        ),
    )


@pytest.fixture
def agent() -> CrewLogisticsAgent:
    return CrewLogisticsAgent()


async def test_return_shape_has_impact_key(agent: CrewLogisticsAgent) -> None:
    result = await agent.assess(_flight())
    assert set(result.keys()) == {"impact"}


async def test_return_value_is_non_empty_string(agent: CrewLogisticsAgent) -> None:
    result = await agent.assess(_flight())
    assert isinstance(result["impact"], str) and result["impact"]


async def test_normal_returns_no_constraints(agent: CrewLogisticsAgent) -> None:
    result = await agent.assess(_flight(OperationalStatus.NORMAL, fuel=180))
    assert result["impact"] == "No crew or gate constraints detected."


async def test_critical_low_fuel_signals_fuel_critical(
    agent: CrewLogisticsAgent,
) -> None:
    fuel = _FUEL_CRITICAL_THRESHOLD - 1
    result = await agent.assess(_flight(OperationalStatus.CRITICAL, fuel=fuel))
    assert "Fuel critical" in result["impact"]
    assert str(fuel) in result["impact"]


async def test_critical_low_fuel_mentions_gate_conflict(
    agent: CrewLogisticsAgent,
) -> None:
    result = await agent.assess(
        _flight(OperationalStatus.CRITICAL, fuel=_FUEL_CRITICAL_THRESHOLD - 1)
    )
    assert "Gate conflict" in result["impact"]


async def test_critical_adequate_fuel_still_signals_critical(
    agent: CrewLogisticsAgent,
) -> None:
    # A CRITICAL flight with fuel above threshold is still critical — crew duty
    # and gate risk must not be masked by an adequate fuel reading.
    result = await agent.assess(
        _flight(OperationalStatus.CRITICAL, fuel=_FUEL_CRITICAL_THRESHOLD + 30)
    )
    assert result["impact"] != "No crew or gate constraints detected."


async def test_warning_adequate_fuel_signals_monitor(agent: CrewLogisticsAgent) -> None:
    result = await agent.assess(_flight(OperationalStatus.WARNING, fuel=90))
    assert "Fuel adequate" in result["impact"]
    assert "90" in result["impact"]
