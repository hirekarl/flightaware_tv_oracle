import type { FlightState, OperationalStatus } from '../types/flight';

const SEVERITY_ORDER: Record<OperationalStatus, number> = {
  CRITICAL: 0,
  WARNING: 1,
  NORMAL: 2,
};

/** Pure sort: CRITICAL → WARNING → NORMAL. Does not mutate the input array. */
export function sortFlightsBySeverity<T extends FlightState>(flights: T[]): T[] {
  return [...flights].sort(
    (a, b) => SEVERITY_ORDER[a.operationalStatus] - SEVERITY_ORDER[b.operationalStatus]
  );
}
