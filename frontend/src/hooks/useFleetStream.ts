import { useEffect, useState } from 'react';
import type { FlightState } from '../types/flight';

interface FleetStreamState {
  flights: FlightState[];
  loading: boolean;
  error: boolean;
}

function isFlightState(value: unknown): value is FlightState {
  return (
    typeof value === 'object' &&
    value !== null &&
    'flightId' in value &&
    'operationalStatus' in value &&
    'aiAnalysis' in value &&
    'route' in value &&
    'telemetry' in value &&
    'deviationType' in value &&
    'aircraftType' in value
  );
}

function parseFleetEvent(raw: string): FlightState[] {
  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(isFlightState);
  } catch {
    return [];
  }
}

export function useFleetStream(url: string): FleetStreamState {
  const [state, setState] = useState<FleetStreamState>({
    flights: [],
    loading: true,
    error: false,
  });

  useEffect(() => {
    const source = new EventSource(url);

    source.onmessage = (e: MessageEvent<string>) => {
      const flights = parseFleetEvent(e.data);
      // The backend sends full-fleet snapshots every cycle — an empty array
      // indicates a heartbeat or partial flush, not an intentionally empty fleet.
      // Only update state when there is real data to avoid clearing the board.
      if (flights.length > 0) {
        setState({ flights, loading: false, error: false });
      }
    };

    source.onerror = () => {
      setState((prev) => ({
        flights: prev.flights,
        loading: false,
        // Only raise the error flag when there is no fleet data to display.
        // If we already received a snapshot, keep showing it — a transient
        // disconnect should not blank the board for dispatchers.
        error: prev.flights.length === 0,
      }));
    };

    return () => source.close();
  }, [url]);

  return state;
}
