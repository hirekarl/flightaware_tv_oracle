"""Mock fleet data generator for development and local testing."""

import random

from backend.models.flight import (
    AiAnalysis,
    DeviationType,
    FlightState,
    OperationalStatus,
    Route,
    Telemetry,
)

_MOCK_FLEET: list[FlightState] = [
    FlightState(
        flightId="AA123",
        aircraftType="B738",
        route=Route(departure="KJFK", destination="KORD"),
        operationalStatus=OperationalStatus.CRITICAL,
        deviationType=DeviationType.GO_AROUND,
        telemetry=Telemetry(fuelRemainingMin=45, altitude=2400),
        aiAnalysis=AiAnalysis(
            summaryTitle="JFK Runway 22L Aborted Landing",
            rootCause="Windshear alert triggered at decision height.",
            downstreamImpact="Crew timeout risk. Fuel reserves critical in 25 min.",
            recommendedAction="Divert to KMKE (Milwaukee); gate K4 is open.",
        ),
    ),
    FlightState(
        flightId="UA456",
        aircraftType="A320",
        route=Route(departure="KLAX", destination="KSFO"),
        operationalStatus=OperationalStatus.WARNING,
        deviationType=DeviationType.HOLDING_PATTERN,
        telemetry=Telemetry(fuelRemainingMin=90, altitude=8000),
        aiAnalysis=AiAnalysis(
            summaryTitle="SFO Ground Delay — Fog Closure",
            rootCause="Runway 28R ILS approaches suspended; visibility below minimums.",
            downstreamImpact="3 connections at risk. Gate conflict in 40 min.",
            recommendedAction="Hold 20 min; re-evaluate approach clearance window.",
        ),
    ),
    FlightState(
        flightId="DL789",
        aircraftType="B737",
        route=Route(departure="KATL", destination="KMIA"),
        operationalStatus=OperationalStatus.NORMAL,
        deviationType=DeviationType.NONE,
        telemetry=Telemetry(fuelRemainingMin=180, altitude=35000),
        aiAnalysis=AiAnalysis(
            summaryTitle="ATL→MIA — On Schedule",
            rootCause="No deviations detected.",
            downstreamImpact="No downstream disruption.",
            recommendedAction="Continue as filed.",
        ),
    ),
    FlightState(
        flightId="SW202",
        aircraftType="B737",
        route=Route(departure="KDEN", destination="KLAS"),
        operationalStatus=OperationalStatus.WARNING,
        deviationType=DeviationType.DIVERSION,
        telemetry=Telemetry(fuelRemainingMin=60, altitude=12000),
        aiAnalysis=AiAnalysis(
            summaryTitle="DEN→LAS — Weather Diversion",
            rootCause="SIGMET Z4 — severe turbulence along filed route.",
            downstreamImpact="2 crew approaching duty limit. Gate reassignment needed.",
            recommendedAction="Divert via KPHX; coordinate gate C12 with ground ops.",
        ),
    ),
]


def generate_mock_fleet() -> list[FlightState]:
    """Return a shuffled snapshot of mock fleet states."""
    flights = list(_MOCK_FLEET)
    random.shuffle(flights)
    return flights
