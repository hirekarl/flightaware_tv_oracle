"""Tests for RouteAnalyticsAgent.analyze() return shape and routing logic."""

import pytest

from backend.agents.route_analytics import RouteAnalyticsAgent
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
    deviation: DeviationType = DeviationType.NONE,
) -> FlightState:
    return FlightState(
        flightId="TS001",
        aircraftType="B738",
        route=Route(departure="KJFK", destination="KORD"),
        operationalStatus=status,
        deviationType=deviation,
        telemetry=Telemetry(fuelRemainingMin=90, altitude=10000),
        aiAnalysis=AiAnalysis(
            summaryTitle="Test",
            rootCause=".",
            downstreamImpact=".",
            recommendedAction=".",
        ),
    )


@pytest.fixture
def agent() -> RouteAnalyticsAgent:
    return RouteAnalyticsAgent()


async def test_normal_returns_no_deviation(agent: RouteAnalyticsAgent) -> None:
    result = await agent.analyze(_flight(OperationalStatus.NORMAL, DeviationType.NONE))
    assert result["root_cause"] == "No deviations detected."
    assert result["action"] == "Continue as filed."


async def test_return_shape_has_required_keys(agent: RouteAnalyticsAgent) -> None:
    result = await agent.analyze(_flight())
    assert set(result.keys()) == {"root_cause", "action"}


async def test_return_values_are_non_empty_strings(agent: RouteAnalyticsAgent) -> None:
    for status in OperationalStatus:
        for deviation in DeviationType:
            result = await agent.analyze(_flight(status, deviation))
            assert isinstance(result["root_cause"], str) and result["root_cause"]
            assert isinstance(result["action"], str) and result["action"]


async def test_critical_go_around_root_cause(agent: RouteAnalyticsAgent) -> None:
    result = await agent.analyze(
        _flight(OperationalStatus.CRITICAL, DeviationType.GO_AROUND)
    )
    assert "Go-around" in result["root_cause"]
    assert "KORD" in result["root_cause"]


async def test_critical_holding_pattern_root_cause(agent: RouteAnalyticsAgent) -> None:
    result = await agent.analyze(
        _flight(OperationalStatus.CRITICAL, DeviationType.HOLDING_PATTERN)
    )
    assert "Holding" in result["root_cause"]


async def test_critical_diversion_root_cause(agent: RouteAnalyticsAgent) -> None:
    result = await agent.analyze(
        _flight(OperationalStatus.CRITICAL, DeviationType.DIVERSION)
    )
    assert "Diversion" in result["root_cause"]


async def test_critical_action_signals_immediate(agent: RouteAnalyticsAgent) -> None:
    result = await agent.analyze(
        _flight(OperationalStatus.CRITICAL, DeviationType.GO_AROUND)
    )
    assert "Immediate" in result["action"]


async def test_warning_action_signals_monitor(agent: RouteAnalyticsAgent) -> None:
    result = await agent.analyze(
        _flight(OperationalStatus.WARNING, DeviationType.HOLDING_PATTERN)
    )
    assert "Monitor" in result["action"]
