import { useEffect, useRef, useState } from 'react';
import type { FlightState } from '../types/flight';

interface FleetStreamState {
  flights: FlightState[];
  loading: boolean;
  error: boolean;
  reconnecting: boolean;
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
    reconnecting: false,
  });

  // Tracks whether we've ever received real data in this mount.
  // Determines whether an error shows a loading spinner (no data yet)
  // or a reconnecting banner (data already on screen, keep it visible).
  const hasData = useRef(false);

  useEffect(() => {
    let source: EventSource | null = null;
    let pollTimer: ReturnType<typeof setInterval> | null = null;
    let cancelled = false;

    // Derive health URL from the stream URL so we can ping the backend
    // with a cheap GET request to trigger Render's free-tier spin-up.
    const healthUrl = url.replace('/api/fleet/stream', '/health');

    const openStream = () => {
      if (cancelled) return;
      source = new EventSource(url);

      source.onmessage = (e: MessageEvent<string>) => {
        const flights = parseFleetEvent(e.data);
        if (flights.length > 0) {
          hasData.current = true;
          setState({ flights, loading: false, error: false, reconnecting: false });
        }
      };

      source.onerror = () => {
        source?.close();
        source = null;
        if (cancelled) return;
        // If we already had data, keep the board visible and show a
        // reconnecting banner. If not, stay in loading state.
        setState((prev) => ({
          ...prev,
          loading: !hasData.current,
          error: false,
          reconnecting: hasData.current,
        }));
        startHealthPoll();
      };
    };

    const startHealthPoll = () => {
      // Guard against accumulating multiple intervals if onerror fires again
      // while a poll is already running.
      if (pollTimer !== null || cancelled) return;
      pollTimer = setInterval(() => {
        fetch(healthUrl)
          .then((res) => {
            if (res.ok && !cancelled) {
              clearInterval(pollTimer!);
              pollTimer = null;
              openStream();
            }
          })
          .catch(() => {
            // backend still sleeping — keep polling
          });
      }, 15000);
    };

    openStream();

    return () => {
      cancelled = true;
      source?.close();
      if (pollTimer !== null) clearInterval(pollTimer);
    };
  }, [url]);

  return state;
}
