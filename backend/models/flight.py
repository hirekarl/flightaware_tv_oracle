"""Pydantic v2 models enforcing the frontend/backend JSON data contract.

The `FlightState` model is the canonical schema. All backend endpoints must
return typed instances — never raw dicts. All frontend types in
`frontend/src/types/flight.ts` must mirror these fields exactly.
"""

from enum import StrEnum

from pydantic import BaseModel, Field


class OperationalStatus(StrEnum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class DeviationType(StrEnum):
    GO_AROUND = "GO_AROUND"
    HOLDING_PATTERN = "HOLDING_PATTERN"
    DIVERSION = "DIVERSION"
    NONE = "NONE"


class Route(BaseModel):
    departure: str = Field(min_length=3, max_length=4)
    destination: str = Field(min_length=3, max_length=4)


class Telemetry(BaseModel):
    fuelRemainingMin: int = Field(ge=0)
    altitude: int = Field(ge=0)


class AiAnalysis(BaseModel):
    summaryTitle: str
    rootCause: str
    downstreamImpact: str
    recommendedAction: str


class FlightState(BaseModel):
    """Root data contract model.

    Both backend and frontend validate against this shape.
    """

    flightId: str
    aircraftType: str
    route: Route
    operationalStatus: OperationalStatus
    deviationType: DeviationType
    telemetry: Telemetry
    aiAnalysis: AiAnalysis
