import React from 'react';
import type { FlightState } from '../types/flight';
import FlightCard from './FlightCard';

interface Props {
  flights: FlightState[];
  onFlightClick?: (flight: FlightState) => void;
}

function getDepartTime(flight: FlightState): string {
  const f = flight as FlightState & { departTime?: string };
  return f.departTime ?? '—';
}

const GRID = '2fr 1fr 1fr 1fr';

const headerCell: React.CSSProperties = {
  padding: '6px 12px',
  color: '#8fa8c8',
  fontSize: '0.7rem',
  letterSpacing: '0.08em',
  textAlign: 'left',
};

const dataCell: React.CSSProperties = {
  padding: '6px 12px',
  fontSize: '0.85rem',
  color: '#fff',
  whiteSpace: 'nowrap',
};

const departCell: React.CSSProperties = {
  padding: '6px 12px',
  fontSize: '0.85rem',
  color: '#fff',
  whiteSpace: 'nowrap',
};

export default function MockFlightBoard({ flights, onFlightClick }: Props) {
  if (flights.length === 0) {
    return (
      <p style={{ color: '#8fa8c8', padding: '24px', textAlign: 'center' }}>
        No flights to display
      </p>
    );
  }

  return (
    <div style={{ width: '100%' }}>
      {/* Column headers */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: GRID,
          borderBottom: '1px solid #2A3E6B',
          paddingBottom: '4px',
        }}
      >
        <span style={headerCell}>IDENT</span>
        <span style={headerCell}>TYPE</span>
        <span style={headerCell}>TO</span>
        <span style={headerCell}>DEPART</span>
      </div>

      {/* Section label */}
      <div
        style={{
          color: '#8fa8c8',
          fontSize: '0.7rem',
          padding: '6px 12px',
          letterSpacing: '0.06em',
          borderBottom: '1px solid #2A3E6B',
          textTransform: 'uppercase',
        }}
      >
        Scheduled Departures
      </div>

      {/* Flight rows — each column is a separate grid cell */}
      {flights.map((flight, idx) => (
        <div
          key={flight.flightId}
          role="button"
          tabIndex={0}
          onClick={() => onFlightClick?.(flight)}
          onKeyDown={(e) => e.key === 'Enter' && onFlightClick?.(flight)}
          style={{
            display: 'grid',
            gridTemplateColumns: GRID,
            alignItems: 'center',
            background: idx % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.03)',
            borderBottom: '1px solid rgba(42,62,107,0.5)',
            cursor: onFlightClick ? 'pointer' : undefined,
          }}
        >
          <FlightCard flight={flight} />
          <span style={dataCell}>{flight.aircraftType}</span>
          <span style={dataCell}>{flight.route.destination}</span>
          <span style={departCell}>{getDepartTime(flight)}</span>
        </div>
      ))}
    </div>
  );
}
