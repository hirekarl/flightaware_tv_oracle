import { describe, it, expect } from 'vitest';
import { sortFlightsBySeverity } from './sortFlights';
import type { FlightState } from '../types/flight';

const make = (
  flightId: string,
  status: FlightState['operationalStatus']
): FlightState => ({
  flightId,
  aircraftType: 'B737',
  route: { departure: 'KJFK', destination: 'KLAX' },
  operationalStatus: status,
  deviationType: 'NONE',
  telemetry: { fuelRemainingMin: 120, altitude: 35000 },
  aiAnalysis: {
    summaryTitle: 'OK',
    rootCause: 'None',
    downstreamImpact: 'None',
    recommendedAction: 'No action',
  },
});

describe('sortFlightsBySeverity', () => {
  it('sorts CRITICAL before WARNING before NORMAL', () => {
    const input = [make('A', 'NORMAL'), make('B', 'CRITICAL'), make('C', 'WARNING')];
    const result = sortFlightsBySeverity(input);
    expect(result.map((f) => f.operationalStatus)).toEqual([
      'CRITICAL',
      'WARNING',
      'NORMAL',
    ]);
  });

  it('does not mutate the original array', () => {
    const input = [make('A', 'NORMAL'), make('B', 'CRITICAL')];
    sortFlightsBySeverity(input);
    expect(input[0].operationalStatus).toBe('NORMAL');
  });

  it('preserves relative order within the same status', () => {
    const input = [make('A', 'CRITICAL'), make('B', 'CRITICAL'), make('C', 'NORMAL')];
    const result = sortFlightsBySeverity(input);
    expect(result[0].flightId).toBe('A');
    expect(result[1].flightId).toBe('B');
  });
});
