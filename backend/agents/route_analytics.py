"""Route Analytics Agent — telemetry anomaly detection and weather/runway mock data."""

from backend.models.flight import DeviationType, FlightState, OperationalStatus


class RouteAnalyticsAgent:
    """Reads telemetry anomalies and queries external weather/runway mock data.

    Returns structured root-cause and recommended-action strings for the
    Coordinator to compile into an `AiAnalysis` payload.
    """

    async def analyze(self, flight: FlightState) -> dict[str, str]:
        """Assess telemetry and deviation type; return root cause and action.

        Args:
            flight: The validated `FlightState` to analyze.

        Returns:
            A dict with keys ``root_cause`` and ``action``.
        """
        if flight.operationalStatus == OperationalStatus.CRITICAL:
            return {
                "root_cause": self._assess_deviation(flight),
                "action": f"Immediate coordination required for {flight.flightId}.",
            }

        if flight.operationalStatus == OperationalStatus.WARNING:
            return {
                "root_cause": self._assess_deviation(flight),
                "action": f"Monitor {flight.flightId} closely; prepare contingency.",
            }

        return {
            "root_cause": "No deviations detected.",
            "action": "Continue as filed.",
        }

    def _assess_deviation(self, flight: FlightState) -> str:
        match flight.deviationType:
            case DeviationType.GO_AROUND:
                return f"Go-around initiated on approach to {flight.route.destination}."
            case DeviationType.HOLDING_PATTERN:
                return f"Holding pattern near {flight.route.destination}; ATC delay."
            case DeviationType.DIVERSION:
                return f"Diversion in progress from {flight.route.destination} route."
            case _:
                return "Anomaly type unclassified."
