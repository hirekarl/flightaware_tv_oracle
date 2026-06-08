/**
 * TypeScript mirror of `backend/models/flight.py`.
 * All fields are immutable. Never use `any` in components that consume these types.
 */

export type OperationalStatus = 'NORMAL' | 'WARNING' | 'CRITICAL';

export type DeviationType =
  | 'GO_AROUND'
  | 'HOLDING_PATTERN'
  | 'DIVERSION'
  | 'NONE';

export interface Route {
  readonly departure: string;
  readonly destination: string;
}

export interface Telemetry {
  readonly fuelRemainingMin: number;
  readonly altitude: number;
}

export interface AiAnalysis {
  readonly summaryTitle: string;
  readonly rootCause: string;
  readonly downstreamImpact: string;
  readonly recommendedAction: string;
}

export interface FlightState {
  readonly flightId: string;
  readonly aircraftType: string;
  readonly route: Route;
  readonly operationalStatus: OperationalStatus;
  readonly deviationType: DeviationType;
  readonly telemetry: Telemetry;
  readonly aiAnalysis: AiAnalysis;
}
