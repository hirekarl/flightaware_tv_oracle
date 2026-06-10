import React from 'react';
import type { MockFlightEntry } from '../fixtures/mockFlights';
import FlightCard from './FlightCard';

interface Props {
  flights: MockFlightEntry[];
}

const headerCell: React.CSSProperties = {
  padding: '6px 12px',
  color: '#8fa8c8',
  fontSize: '0.7rem',
  letterSpacing: '0.08em',
  textAlign: 'left',
};

const departCell: React.CSSProperties = {
  padding: '4px 12px',
  fontSize: '0.85rem',
  color: '#fff',
  whiteSpace: 'nowrap',
};

export default function MockFlightBoard({ flights }: Props) {
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
          gridTemplateColumns: '2fr 1fr 1fr 1fr',
          borderBottom: '1px solid #1e3a5f',
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
          borderBottom: '1px solid #1e3a5f',
          textTransform: 'uppercase',
        }}
      >
        Scheduled Departures
      </div>

      {/* Flight rows — FlightCard renders IDENT + TYPE + DESTINATION */}
      {flights.map((flight, idx) => (
        <div
          key={flight.flightId}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: idx % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.03)',
            borderBottom: '1px solid rgba(30,58,95,0.5)',
          }}
        >
          <FlightCard flight={flight} />
          <span style={departCell}>{flight.departTime}</span>
        </div>
      ))}
    </div>
  );
}
