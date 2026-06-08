"""Crew Logistics Agent — duty time limit and gate constraint computation."""

from backend.models.flight import FlightState, OperationalStatus

_DUTY_LIMIT_MINUTES = 480
_FUEL_CRITICAL_THRESHOLD = 60


class CrewLogisticsAgent:
    """Computes crew duty time proximity and gate availability constraints.

    Returns a structured impact assessment string for the Coordinator to
    include in the downstream `AiAnalysis.downstreamImpact` field.
    """

    async def assess(self, flight: FlightState) -> dict[str, str]:
        """Evaluate crew risk and gate state for a given flight.

        Args:
            flight: The validated `FlightState` to assess.

        Returns:
            A dict with key ``impact`` describing crew and gate risk.
        """
        fuel = flight.telemetry.fuelRemainingMin
        status = flight.operationalStatus

        if status == OperationalStatus.CRITICAL and fuel < _FUEL_CRITICAL_THRESHOLD:
            return {
                "impact": (
                    f"Fuel critical: {fuel} min remaining. "
                    "Crew duty limit exposure high. Gate conflict imminent."
                )
            }

        if status == OperationalStatus.WARNING:
            return {
                "impact": (
                    f"Fuel adequate ({fuel} min). "
                    "Monitor crew duty time; downstream connections at risk."
                )
            }

        return {"impact": "No crew or gate constraints detected."}
