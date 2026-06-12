import type { FlightState, OperationalStatus } from '../types/flight';

const SEVERITY_ORDER: Record<OperationalStatus, number> = {
  CRITICAL: 0,
  WARNING: 1,
  NORMAL: 2,
};

/**
 * Sorts flights by operational severity (CRITICAL → WARNING → NORMAL).
 *
 * Dispatchers need the highest-risk flights at the top of the list, not
 * sorted by departure time (the default FlightAware TV ordering). This is
 * a pure frontend transform — no backend or data contract changes required.
 * FlightState.operationalStatus is already provided by the SSE stream.
 */
export function sortFlightsBySeverity<T extends FlightState>(flights: T[]): T[] {
  return [...flights].sort(
    (a, b) => SEVERITY_ORDER[a.operationalStatus] - SEVERITY_ORDER[b.operationalStatus]
  );
}
