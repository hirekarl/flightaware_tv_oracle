"""Tests for CoordinatorAgent.analyze() — orchestration and return shape."""

from unittest.mock import AsyncMock, patch

import pytest

from backend.agents.coordinator import CoordinatorAgent
from backend.models.flight import (
    AiAnalysis,
    DeviationType,
    FlightState,
    OperationalStatus,
    Route,
    Telemetry,
)

_MOCK_ANALYSIS = AiAnalysis(
    summaryTitle="AI-Generated Title",
    rootCause="AI-identified root cause.",
    downstreamImpact="AI-assessed downstream impact.",
    recommendedAction="AI-recommended action.",
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
            summaryTitle="Placeholder",
            rootCause="Placeholder.",
            downstreamImpact="Placeholder.",
            recommendedAction="Placeholder.",
        ),
    }
    return FlightState(**{**defaults, **overrides})


@pytest.fixture
def mock_llm_client() -> AsyncMock:
    client = AsyncMock()
    client.create.return_value = _MOCK_ANALYSIS
    return client


async def test_coordinator_analyze_returns_ai_analysis_instance(
    mock_llm_client: AsyncMock,
) -> None:
    with patch(
        "backend.agents.coordinator.instructor.from_provider",
        return_value=mock_llm_client,
    ):
        agent = CoordinatorAgent()
        result = await agent.analyze(_make_flight())
    assert isinstance(result, AiAnalysis)


async def test_coordinator_analyze_all_fields_non_empty(
    mock_llm_client: AsyncMock,
) -> None:
    with patch(
        "backend.agents.coordinator.instructor.from_provider",
        return_value=mock_llm_client,
    ):
        agent = CoordinatorAgent()
        result = await agent.analyze(_make_flight())
    assert result.summaryTitle
    assert result.rootCause
    assert result.downstreamImpact
    assert result.recommendedAction


async def test_coordinator_calls_route_agent(mock_llm_client: AsyncMock) -> None:
    with patch(
        "backend.agents.coordinator.instructor.from_provider",
        return_value=mock_llm_client,
    ):
        agent = CoordinatorAgent()
        route_spy = AsyncMock(return_value={"root_cause": "test", "action": "test"})
        agent._route.analyze = route_spy
        await agent.analyze(_make_flight())
    route_spy.assert_called_once()


async def test_coordinator_calls_crew_agent(mock_llm_client: AsyncMock) -> None:
    with patch(
        "backend.agents.coordinator.instructor.from_provider",
        return_value=mock_llm_client,
    ):
        agent = CoordinatorAgent()
        crew_spy = AsyncMock(return_value={"impact": "test"})
        agent._crew.assess = crew_spy
        await agent.analyze(_make_flight())
    crew_spy.assert_called_once()


async def test_coordinator_passes_flight_to_subagents(
    mock_llm_client: AsyncMock,
) -> None:
    flight = _make_flight()
    with patch(
        "backend.agents.coordinator.instructor.from_provider",
        return_value=mock_llm_client,
    ):
        agent = CoordinatorAgent()
        route_spy = AsyncMock(return_value={"root_cause": "r", "action": "a"})
        crew_spy = AsyncMock(return_value={"impact": "i"})
        agent._route.analyze = route_spy
        agent._crew.assess = crew_spy
        await agent.analyze(flight)
    route_spy.assert_called_once_with(flight)
    crew_spy.assert_called_once_with(flight)


async def test_coordinator_calls_instructor_with_ai_analysis_response_model(
    mock_llm_client: AsyncMock,
) -> None:
    with patch(
        "backend.agents.coordinator.instructor.from_provider",
        return_value=mock_llm_client,
    ):
        agent = CoordinatorAgent()
        await agent.analyze(_make_flight())
    call_kwargs = mock_llm_client.create.call_args.kwargs
    assert call_kwargs["response_model"] is AiAnalysis
    assert call_kwargs["messages"][0]["role"] == "user"
    assert len(call_kwargs["messages"][0]["content"]) > 0


async def test_coordinator_prompt_includes_flight_id(
    mock_llm_client: AsyncMock,
) -> None:
    flight = _make_flight(flightId="UA999")
    with patch(
        "backend.agents.coordinator.instructor.from_provider",
        return_value=mock_llm_client,
    ):
        agent = CoordinatorAgent()
        await agent.analyze(flight)
    prompt = mock_llm_client.create.call_args.kwargs["messages"][0]["content"]
    assert "UA999" in prompt
