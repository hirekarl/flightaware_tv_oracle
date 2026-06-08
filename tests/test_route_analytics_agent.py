"""Tests for RouteAnalyticsAgent.analyze() return shape and behavior."""

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
def agent() -> RouteAnalyticsAgent:
    return RouteAnalyticsAgent()


async def test_analyze_critical_returns_root_cause_and_action_keys(
    agent: RouteAnalyticsAgent,
) -> None:
    result = await agent.analyze(
        _make_flight(operationalStatus=OperationalStatus.CRITICAL)
    )
    assert set(result.keys()) == {"root_cause", "action"}


async def test_analyze_warning_returns_root_cause_and_action_keys(
    agent: RouteAnalyticsAgent,
) -> None:
    result = await agent.analyze(
        _make_flight(operationalStatus=OperationalStatus.WARNING)
    )
    assert set(result.keys()) == {"root_cause", "action"}


async def test_analyze_normal_returns_root_cause_and_action_keys(
    agent: RouteAnalyticsAgent,
) -> None:
    result = await agent.analyze(
        _make_flight(operationalStatus=OperationalStatus.NORMAL)
    )
    assert set(result.keys()) == {"root_cause", "action"}


async def test_analyze_all_values_are_non_empty_strings(
    agent: RouteAnalyticsAgent,
) -> None:
    for status in OperationalStatus:
        result = await agent.analyze(_make_flight(operationalStatus=status))
        assert all(isinstance(v, str) and v for v in result.values()), (
            f"Expected non-empty strings for status {status}, got {result}"
        )


async def test_analyze_critical_go_around_mentions_destination(
    agent: RouteAnalyticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.CRITICAL,
        deviationType=DeviationType.GO_AROUND,
    )
    result = await agent.analyze(flight)
    assert flight.route.destination in result["root_cause"]


async def test_analyze_critical_holding_pattern_mentions_destination(
    agent: RouteAnalyticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.CRITICAL,
        deviationType=DeviationType.HOLDING_PATTERN,
    )
    result = await agent.analyze(flight)
    assert flight.route.destination in result["root_cause"]


async def test_analyze_critical_diversion_mentions_destination(
    agent: RouteAnalyticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.CRITICAL,
        deviationType=DeviationType.DIVERSION,
    )
    result = await agent.analyze(flight)
    assert flight.route.destination in result["root_cause"]


async def test_analyze_critical_action_requires_immediate_coordination(
    agent: RouteAnalyticsAgent,
) -> None:
    result = await agent.analyze(
        _make_flight(operationalStatus=OperationalStatus.CRITICAL)
    )
    assert "Immediate" in result["action"]


async def test_analyze_warning_action_mentions_monitor(
    agent: RouteAnalyticsAgent,
) -> None:
    result = await agent.analyze(
        _make_flight(
            operationalStatus=OperationalStatus.WARNING,
            deviationType=DeviationType.HOLDING_PATTERN,
        )
    )
    assert "Monitor" in result["action"]


async def test_analyze_normal_reports_no_deviations(
    agent: RouteAnalyticsAgent,
) -> None:
    flight = _make_flight(
        operationalStatus=OperationalStatus.NORMAL,
        deviationType=DeviationType.NONE,
    )
    result = await agent.analyze(flight)
    assert result["root_cause"] == "No deviations detected."
    assert result["action"] == "Continue as filed."
