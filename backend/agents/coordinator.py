"""Coordinator Agent — orchestrates Route and Crew agents, validates output schema."""

import asyncio

import instructor

from backend.agents.crew_logistics import CrewLogisticsAgent
from backend.agents.route_analytics import RouteAnalyticsAgent
from backend.models.flight import AiAnalysis, FlightState

_MODEL = "google/gemini-2.5-flash"


def _build_prompt(
    flight: FlightState,
    route_data: dict[str, str],
    crew_data: dict[str, str],
) -> str:
    return (
        f"Flight {flight.flightId} ({flight.aircraftType}) "
        f"{flight.route.departure}→{flight.route.destination} "
        f"is {flight.operationalStatus} with deviation: {flight.deviationType}.\n\n"
        f"Telemetry: {flight.telemetry.fuelRemainingMin} min fuel remaining, "
        f"altitude {flight.telemetry.altitude} ft.\n\n"
        f"Route analysis: {route_data}\n"
        f"Crew assessment: {crew_data}\n\n"
        "Return a concise operational brief for the dispatcher. "
        "summaryTitle should be one line. rootCause, downstreamImpact, and "
        "recommendedAction should each be a single dense sentence."
    )


class CoordinatorAgent:
    """Delegates analysis to RouteAnalyticsAgent and CrewLogisticsAgent.

    Compiles their outputs into a validated `AiAnalysis` model via Instructor +
    Gemini. Reads GOOGLE_API_KEY from the environment automatically via the
    google-genai SDK. This is the only agent the API layer interacts with directly.
    """

    def __init__(self) -> None:
        self._route = RouteAnalyticsAgent()
        self._crew = CrewLogisticsAgent()
        # from_provider reads GOOGLE_API_KEY from env; async_client=True enables
        # native await-able calls without blocking the FastAPI event loop.
        self._client = instructor.from_provider(_MODEL, async_client=True)

    async def analyze(self, flight: FlightState) -> AiAnalysis:
        """Orchestrate subagent analysis and return a validated `AiAnalysis`.

        Args:
            flight: The validated `FlightState` requiring analysis.

        Returns:
            A Pydantic `AiAnalysis` model validated against the data contract.
        """
        route_data, crew_data = await asyncio.gather(
            self._route.analyze(flight),
            self._crew.assess(flight),
        )

        prompt = _build_prompt(flight, route_data, crew_data)

        return await self._client.create(
            response_model=AiAnalysis,
            messages=[{"role": "user", "content": prompt}],
        )
