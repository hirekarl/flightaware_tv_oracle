import { useEffect, useState } from 'react';
import type { FlightState } from '../types/flight';

interface FleetStreamState {
  flights: FlightState[];
  loading: boolean;
}

function isFlightState(value: unknown): value is FlightState {
  return (
    typeof value === 'object' &&
    value !== null &&
    'flightId' in value &&
    'operationalStatus' in value &&
    'aiAnalysis' in value
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
  const [state, setState] = useState<FleetStreamState>({ flights: [], loading: true });

  useEffect(() => {
    const source = new EventSource(url);

    source.onmessage = (e: MessageEvent<string>) => {
      const flights = parseFleetEvent(e.data);
      setState({ flights, loading: false });
    };

    source.onerror = () => {
      setState((prev) => ({ ...prev, loading: false }));
    };

    return () => source.close();
  }, [url]);

  return state;
}
