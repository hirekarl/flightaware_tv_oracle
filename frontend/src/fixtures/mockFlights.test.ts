import { describe, it, expect } from 'vitest';
import { mockFlights } from './mockFlights';
import type { MockFlightEntry } from './mockFlights';
import type { FlightState } from '../types/flight';

const VALID_STATUSES: FlightState['operationalStatus'][] = [
  'NORMAL',
  'WARNING',
  'CRITICAL',
];
const VALID_DEVIATIONS: FlightState['deviationType'][] = [
  'GO_AROUND',
  'HOLDING_PATTERN',
  'DIVERSION',
  'NONE',
];

describe('mockFlights fixture', () => {
  it('exports at least 5 entries', () => {
    expect(mockFlights.length).toBeGreaterThanOrEqual(5);
  });

  it('each entry satisfies the full FlightState contract', () => {
    mockFlights.forEach((flight: MockFlightEntry) => {
      expect(typeof flight.flightId).toBe('string');
      expect(flight.flightId.length).toBeGreaterThan(0);
      expect(typeof flight.aircraftType).toBe('string');
      expect(typeof flight.route.departure).toBe('string');
      expect(typeof flight.route.destination).toBe('string');
      expect(VALID_STATUSES).toContain(flight.operationalStatus);
      expect(VALID_DEVIATIONS).toContain(flight.deviationType);
      expect(typeof flight.telemetry.fuelRemainingMin).toBe('number');
      expect(flight.telemetry.fuelRemainingMin).toBeGreaterThanOrEqual(0);
      expect(typeof flight.telemetry.altitude).toBe('number');
      expect(flight.telemetry.altitude).toBeGreaterThanOrEqual(0);
      expect(typeof flight.aiAnalysis.summaryTitle).toBe('string');
      expect(typeof flight.aiAnalysis.rootCause).toBe('string');
      expect(typeof flight.aiAnalysis.downstreamImpact).toBe('string');
      expect(typeof flight.aiAnalysis.recommendedAction).toBe('string');
    });
  });

  it('each entry has a non-empty departTime string for the UI shell', () => {
    mockFlights.forEach((flight: MockFlightEntry) => {
      expect(typeof flight.departTime).toBe('string');
      expect(flight.departTime.length).toBeGreaterThan(0);
    });
  });

  it('fixture covers all three operational statuses', () => {
    const statuses = new Set(mockFlights.map((f) => f.operationalStatus));
    expect(statuses.has('NORMAL')).toBe(true);
    expect(statuses.has('WARNING')).toBe(true);
    expect(statuses.has('CRITICAL')).toBe(true);
  });
});
