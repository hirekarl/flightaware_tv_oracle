"""Demo scenario engine for FlightAware TV.

Defines a 6-beat JFK weather/ATC crisis that a presenter can advance manually
via POST /demo/next. generate_mock_fleet() delegates to the module-level
ScenarioEngine singleton so all existing call sites (main.py, tests) remain
unchanged.
"""

from typing import ClassVar

from backend.models.flight import (
    AiAnalysis,
    DeviationType,
    FlightState,
    OperationalStatus,
    Route,
    Telemetry,
)

_PENDING = AiAnalysis(
    summaryTitle="Pending AI analysis",
    rootCause="—",
    downstreamImpact="—",
    recommendedAction="—",
)


def _f(
    flight_id: str,
    aircraft_type: str,
    departure: str,
    destination: str,
    status: OperationalStatus,
    deviation: DeviationType,
    fuel: int,
    altitude: int,
) -> FlightState:
    return FlightState(
        flightId=flight_id,
        aircraftType=aircraft_type,
        route=Route(departure=departure, destination=destination),
        operationalStatus=status,
        deviationType=deviation,
        telemetry=Telemetry(fuelRemainingMin=fuel, altitude=altitude),
        aiAnalysis=_PENDING,
    )


N = OperationalStatus.NORMAL
W = OperationalStatus.WARNING
C = OperationalStatus.CRITICAL
NONE = DeviationType.NONE
HOLD = DeviationType.HOLDING_PATTERN
GO = DeviationType.GO_AROUND
DIV = DeviationType.DIVERSION


class ScenarioEngine:
    """Advances a scripted 6-beat demo scenario on demand."""

    _BEAT_NAMES: ClassVar[list[str]] = [
        "Normal Ops — Background Disruptions",
        "AA123 Enters Hold — JFK Weather",
        "AA123 Misses Approach — SW202 Clears",
        "UA456 Diverts — Cascade Visible",
        "AA123 Diverts — NK501 Goes Critical",
        "AA123/UA456 Recover — NK501 Cliffhanger",
    ]

    _BEATS: ClassVar[list[list[FlightState]]] = [
        # Beat 0 — Normal ops, two background disruptions
        [
            _f("AA123", "B738", "KJFK", "KORD", N, NONE, 140, 35000),
            _f("UA456", "A320", "KLAX", "KSFO", W, HOLD, 95, 9000),
            _f("DL789", "B737", "KATL", "KMIA", N, NONE, 185, 35000),
            _f("SW202", "B737", "KDEN", "KLAS", W, DIV, 62, 11000),
            _f("NK501", "B738", "KEWR", "KBOS", N, NONE, 90, 35000),
        ],
        # Beat 1 — AA123 enters hold; fuel starts to matter
        [
            _f("AA123", "B738", "KJFK", "KORD", W, HOLD, 110, 8000),
            _f("UA456", "A320", "KLAX", "KSFO", W, HOLD, 82, 9000),
            _f("DL789", "B737", "KATL", "KMIA", N, NONE, 160, 35000),
            _f("SW202", "B737", "KDEN", "KLAS", W, DIV, 52, 11000),
            _f("NK501", "B738", "KEWR", "KBOS", N, NONE, 78, 35000),
        ],
        # Beat 2 — AA123 misses approach; SW202 resolves
        [
            _f("AA123", "B738", "KJFK", "KORD", W, GO, 85, 2500),
            _f("UA456", "A320", "KLAX", "KSFO", W, HOLD, 68, 9000),
            _f("DL789", "B737", "KATL", "KMIA", N, NONE, 135, 35000),
            _f("SW202", "B737", "KDEN", "KLAS", N, NONE, 78, 28000),
            _f("NK501", "B738", "KEWR", "KBOS", N, NONE, 66, 35000),
        ],
        # Beat 3 — UA456 diverts; cascade begins; NK501 joins hold
        [
            _f("AA123", "B738", "KJFK", "KORD", C, GO, 55, 2500),
            _f("UA456", "A320", "KLAX", "KSFO", C, DIV, 52, 14000),
            _f("DL789", "B737", "KATL", "KMIA", N, NONE, 110, 35000),
            _f("SW202", "B737", "KDEN", "KLAS", N, NONE, 68, 35000),
            _f("NK501", "B738", "KEWR", "KBOS", W, HOLD, 54, 7500),
        ],
        # Beat 4 — AA123 diverts; NK501 goes critical; DL789 enters hold
        [
            _f("AA123", "B738", "KJFK", "KORD", C, DIV, 38, 12000),
            _f("UA456", "A320", "KLAX", "KSFO", C, DIV, 41, 14000),
            _f("DL789", "B737", "KATL", "KMIA", W, HOLD, 85, 7000),
            _f("SW202", "B737", "KDEN", "KLAS", N, NONE, 58, 35000),
            _f("NK501", "B738", "KEWR", "KBOS", C, HOLD, 38, 7500),
        ],
        # Beat 5 — AA123/UA456 recover at alternates; NK501 still critical (cliffhanger)
        [
            _f("AA123", "B738", "KJFK", "KORD", N, NONE, 95, 18000),
            _f("UA456", "A320", "KLAX", "KSFO", N, NONE, 88, 22000),
            _f("DL789", "B737", "KATL", "KMIA", W, HOLD, 72, 7000),
            _f("SW202", "B737", "KDEN", "KLAS", N, NONE, 48, 35000),
            _f("NK501", "B738", "KEWR", "KBOS", C, HOLD, 28, 7500),
        ],
    ]

    def __init__(self) -> None:
        self._beat_index: int = 0

    @property
    def beat_index(self) -> int:
        return self._beat_index

    @property
    def beat_name(self) -> str:
        return self._BEAT_NAMES[self._beat_index]

    def current_beat(self) -> list[FlightState]:
        return list(self._BEATS[self._beat_index])

    def advance(self) -> tuple[int, str]:
        self._beat_index = (self._beat_index + 1) % len(self._BEATS)
        return self._beat_index, self.beat_name

    def reset(self) -> None:
        self._beat_index = 0


_engine = ScenarioEngine()


def generate_mock_fleet() -> list[FlightState]:
    """Return the current scenario beat's fleet snapshot."""
    return _engine.current_beat()
