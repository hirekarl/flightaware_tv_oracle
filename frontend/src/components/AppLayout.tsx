import React, { useState, useEffect } from 'react';
import MockFlightBoard from './MockFlightBoard';
import MapPanel from './MapPanel';
import AiImpactDrawer from './AiImpactDrawer';
import { sortFlightsBySeverity } from '../utils/sortFlights';
import { useFleetStream } from '../hooks/useFleetStream';
import type { FlightState } from '../types/flight';

const API_URL =
  (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000';

type Tab = 'map' | 'flights';

interface FlightsPanelProps {
  flights: FlightState[];
  loading: boolean;
}

function FlightsPanel({ flights, loading }: FlightsPanelProps) {
  const [selectedFlight, setSelectedFlight] = useState<FlightState | null>(null);

  let content: React.ReactNode;
  if (loading) {
    content = (
      <p style={{ color: '#8fa8c8', padding: '24px', textAlign: 'center' }}>
        Connecting to live feed…
      </p>
    );
  } else if (flights.length === 0) {
    content = (
      <p style={{ color: '#8fa8c8', padding: '24px', textAlign: 'center' }}>
        No active disruptions
      </p>
    );
  } else {
    content = (
      <MockFlightBoard
        flights={sortFlightsBySeverity(flights)}
        onFlightClick={setSelectedFlight}
      />
    );
  }

  return (
    <div
      data-testid="flights-panel"
      style={{
        background: 'var(--fa-navy)',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        overflow: 'hidden',
      }}
    >
      <Header />
      <div style={{ flex: 1, overflowY: 'auto' }}>{content}</div>
      <AiImpactDrawer flight={selectedFlight} onClose={() => setSelectedFlight(null)} />
    </div>
  );
}

function Header() {
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const dateStr = now.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });
  const timeStr = now.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 16px',
        borderBottom: '1px solid #2A3E6B',
        flexShrink: 0,
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          color: 'var(--fa-blue)',
        }}
      >
        <span aria-hidden="true">✈</span>
        <h1
          style={{
            margin: 0,
            fontSize: '1rem',
            fontWeight: 700,
            letterSpacing: '0.04em',
          }}
        >
          FlightAware TV
        </h1>
      </div>
      <div style={{ textAlign: 'right', color: '#fff', fontSize: '0.8rem' }}>
        <div style={{ color: 'var(--fa-blue)', fontWeight: 600 }}>{dateStr}</div>
        <div style={{ fontVariantNumeric: 'tabular-nums' }}>{timeStr}</div>
      </div>
    </div>
  );
}

export default function AppLayout() {
  const { flights, loading } = useFleetStream(`${API_URL}/api/fleet/stream`);
  const [isMobile, setIsMobile] = useState(
    () => window.matchMedia('(max-width: 1023px)').matches
  );
  const [activeTab, setActiveTab] = useState<Tab>('map');

  useEffect(() => {
    const mq = window.matchMedia('(max-width: 1023px)');
    const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  if (!isMobile) {
    return (
      <div
        style={{
          display: 'flex',
          height: '100vh',
          background: 'var(--fa-navy)',
          overflow: 'hidden',
        }}
      >
        <div style={{ flex: '0 0 60%', height: '100vh' }}>
          <MapPanel flights={flights} />
        </div>
        <div style={{ flex: '0 0 40%', height: '100%', overflowY: 'auto' }}>
          <FlightsPanel flights={flights} loading={loading} />
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        background: 'var(--fa-navy)',
      }}
    >
      {/* Tab bar */}
      <div
        role="tablist"
        style={{
          display: 'flex',
          background: 'var(--fa-navy)',
          borderBottom: '1px solid #2A3E6B',
          flexShrink: 0,
        }}
      >
        <button
          role="tab"
          aria-selected={activeTab === 'map'}
          onClick={() => setActiveTab('map')}
          style={{
            flex: 1,
            padding: '12px',
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            color: activeTab === 'map' ? 'var(--fa-blue)' : '#2A3E6B',
            borderBottom:
              activeTab === 'map'
                ? '2px solid var(--fa-blue)'
                : '2px solid transparent',
            fontWeight: activeTab === 'map' ? 700 : 400,
            fontSize: '0.9rem',
          }}
        >
          Map
        </button>
        <button
          role="tab"
          aria-selected={activeTab === 'flights'}
          onClick={() => setActiveTab('flights')}
          style={{
            flex: 1,
            padding: '12px',
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            color: activeTab === 'flights' ? 'var(--fa-blue)' : '#2A3E6B',
            borderBottom:
              activeTab === 'flights'
                ? '2px solid var(--fa-blue)'
                : '2px solid transparent',
            fontWeight: activeTab === 'flights' ? 700 : 400,
            fontSize: '0.9rem',
          }}
        >
          Flights
        </button>
      </div>

      {/* Tab panels */}
      <div style={{ flex: 1, overflow: 'hidden', height: 'calc(100vh - 48px)' }}>
        {activeTab === 'map' ? (
          <MapPanel flights={flights} />
        ) : (
          <FlightsPanel flights={flights} loading={loading} />
        )}
      </div>
    </div>
  );
}
