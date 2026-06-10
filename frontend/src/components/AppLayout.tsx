import { useState, useEffect } from 'react';
import MockFlightBoard from './MockFlightBoard';
import { mockFlights } from '../fixtures/mockFlights';

type Tab = 'map' | 'flights';

function MapPanel() {
  return (
    <div
      data-testid="map-panel"
      style={{
        flex: 1,
        background: 'var(--fa-map-bg)',
        position: 'relative',
        overflow: 'hidden',
        minHeight: '100%',
      }}
    >
      {/* Static SVG aircraft scattered at approximate US positions */}
      <svg
        viewBox="0 0 100 60"
        style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}
        aria-hidden="true"
      >
        <text x="22" y="18" fontSize="3" fill="#00e676" transform="rotate(-45,22,18)">
          ✈
        </text>
        <text x="35" y="28" fontSize="3" fill="#4dd0e1" transform="rotate(30,35,28)">
          ✈
        </text>
        <text x="55" y="15" fontSize="3" fill="#00e676" transform="rotate(-20,55,15)">
          ✈
        </text>
        <text x="48" y="35" fontSize="3" fill="#00e676" transform="rotate(10,48,35)">
          ✈
        </text>
        <text x="70" y="22" fontSize="3" fill="#4dd0e1" transform="rotate(-35,70,22)">
          ✈
        </text>
        <text x="62" y="42" fontSize="3" fill="#ff5252" transform="rotate(15,62,42)">
          ✈
        </text>
        <text x="30" y="45" fontSize="3" fill="#00e676" transform="rotate(-10,30,45)">
          ✈
        </text>
        <text x="80" y="38" fontSize="3" fill="#4dd0e1" transform="rotate(-50,80,38)">
          ✈
        </text>
      </svg>
    </div>
  );
}

function FlightsPanel() {
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
      <div style={{ flex: 1, overflowY: 'auto' }}>
        <MockFlightBoard flights={mockFlights} />
      </div>
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
        borderBottom: '1px solid #1e3a5f',
        flexShrink: 0,
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          color: 'var(--fa-blue)',
          fontWeight: 700,
          fontSize: '1rem',
          letterSpacing: '0.04em',
        }}
      >
        <span aria-hidden="true">✈</span>
        <span>FlightAware</span>
      </div>
      <div style={{ textAlign: 'right', color: '#fff', fontSize: '0.8rem' }}>
        <div style={{ color: 'var(--fa-blue)', fontWeight: 600 }}>{dateStr}</div>
        <div style={{ fontVariantNumeric: 'tabular-nums' }}>{timeStr}</div>
      </div>
    </div>
  );
}

export default function AppLayout() {
  const isMobile = useState(() => window.matchMedia('(max-width: 1023px)').matches)[0];
  const [activeTab, setActiveTab] = useState<Tab>('map');

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
        <div style={{ flex: '0 0 60%', height: '100%' }}>
          <MapPanel />
        </div>
        <div style={{ flex: '0 0 40%', height: '100%', overflowY: 'auto' }}>
          <FlightsPanel />
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
          borderBottom: '1px solid #1e3a5f',
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
            color: activeTab === 'map' ? 'var(--fa-blue)' : '#8fa8c8',
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
            color: activeTab === 'flights' ? 'var(--fa-blue)' : '#8fa8c8',
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
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {activeTab === 'map' ? <MapPanel /> : <FlightsPanel />}
      </div>
    </div>
  );
}
