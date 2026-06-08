"""Tests for the FlightState Pydantic data contract."""

import pytest
from pydantic import ValidationError

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
            rootCause="Root cause.",
            downstreamImpact="Impact.",
            recommendedAction="Action.",
        ),
    }
    return FlightState(**{**defaults, **overrides})


def test_valid_flight_state() -> None:
    flight = _make_flight()
    assert flight.flightId == "AA123"
    assert flight.operationalStatus == OperationalStatus.CRITICAL
    assert flight.route.departure == "KJFK"


def test_all_operational_statuses_accepted() -> None:
    for status in OperationalStatus:
        flight = _make_flight(operationalStatus=status)
        assert flight.operationalStatus == status


def test_all_deviation_types_accepted() -> None:
    for dev_type in DeviationType:
        flight = _make_flight(deviationType=dev_type)
        assert flight.deviationType == dev_type


def test_telemetry_rejects_negative_fuel() -> None:
    with pytest.raises(ValidationError):
        _make_flight(telemetry=Telemetry(fuelRemainingMin=-1, altitude=0))


def test_telemetry_rejects_negative_altitude() -> None:
    with pytest.raises(ValidationError):
        _make_flight(telemetry=Telemetry(fuelRemainingMin=0, altitude=-1))


def test_route_rejects_short_icao() -> None:
    with pytest.raises(ValidationError):
        _make_flight(route=Route(departure="JF", destination="KORD"))


def test_route_rejects_long_icao() -> None:
    with pytest.raises(ValidationError):
        _make_flight(route=Route(departure="KJFKX", destination="KORD"))


def test_model_serializes_to_contract_shape() -> None:
    flight = _make_flight()
    data = flight.model_dump()
    assert set(data.keys()) == {
        "flightId",
        "aircraftType",
        "route",
        "operationalStatus",
        "deviationType",
        "telemetry",
        "aiAnalysis",
    }
