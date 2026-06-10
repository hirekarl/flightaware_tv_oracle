"""Tests for CoordinatorAgent.analyze() orchestration and output contract."""

from unittest.mock import AsyncMock, MagicMock

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


def _flight(status: OperationalStatus = OperationalStatus.CRITICAL) -> FlightState:
    return FlightState(
        flightId="AA123",
        aircraftType="B738",
        route=Route(departure="KJFK", destination="KORD"),
        operationalStatus=status,
        deviationType=DeviationType.GO_AROUND,
        telemetry=Telemetry(fuelRemainingMin=45, altitude=2400),
        aiAnalysis=AiAnalysis(
            summaryTitle="Stub",
            rootCause=".",
            downstreamImpact=".",
            recommendedAction=".",
        ),
    )


def _mock_client(analysis: AiAnalysis) -> MagicMock:
    client = MagicMock()
    client.create = AsyncMock(return_value=analysis)
    return client


@pytest.fixture
def stub_analysis() -> AiAnalysis:
    return AiAnalysis(
        summaryTitle="JFK Go-Around",
        rootCause="Windshear at decision height.",
        downstreamImpact="Crew timeout risk in 25 min.",
        recommendedAction="Divert to KMKE.",
    )


async def test_returns_ai_analysis_instance(stub_analysis: AiAnalysis) -> None:
    agent = CoordinatorAgent(client=_mock_client(stub_analysis))
    result = await agent.analyze(_flight())
    assert isinstance(result, AiAnalysis)


async def test_returns_analysis_from_client(stub_analysis: AiAnalysis) -> None:
    agent = CoordinatorAgent(client=_mock_client(stub_analysis))
    result = await agent.analyze(_flight())
    assert result.summaryTitle == "JFK Go-Around"
    assert result.rootCause == "Windshear at decision height."


async def test_client_create_called_once(stub_analysis: AiAnalysis) -> None:
    mock = _mock_client(stub_analysis)
    agent = CoordinatorAgent(client=mock)
    await agent.analyze(_flight())
    mock.create.assert_called_once()


async def test_client_called_with_response_model(stub_analysis: AiAnalysis) -> None:
    mock = _mock_client(stub_analysis)
    agent = CoordinatorAgent(client=mock)
    await agent.analyze(_flight())
    call_kwargs = mock.create.call_args.kwargs
    assert call_kwargs["response_model"] is AiAnalysis


async def test_prompt_contains_flight_id(stub_analysis: AiAnalysis) -> None:
    mock = _mock_client(stub_analysis)
    agent = CoordinatorAgent(client=mock)
    await agent.analyze(_flight())
    call_kwargs = mock.create.call_args.kwargs
    prompt = call_kwargs["messages"][0]["content"]
    assert "AA123" in prompt


async def test_prompt_contains_status(stub_analysis: AiAnalysis) -> None:
    mock = _mock_client(stub_analysis)
    agent = CoordinatorAgent(client=mock)
    await agent.analyze(_flight(OperationalStatus.CRITICAL))
    call_kwargs = mock.create.call_args.kwargs
    prompt = call_kwargs["messages"][0]["content"]
    assert "CRITICAL" in prompt
