import type { FlightState } from '../types/flight';

export interface MockFlightEntry extends FlightState {
  readonly departTime: string;
}

// Stub — implementation pending. Tests will fail against this empty array.
export const mockFlights: MockFlightEntry[] = [];
