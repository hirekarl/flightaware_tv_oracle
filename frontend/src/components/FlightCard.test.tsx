import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import FlightCard from './FlightCard';
import type { FlightState } from '../types/flight';

const base: FlightState = {
  flightId: 'AA123',
  aircraftType: 'B737',
  route: { departure: 'KIAD', destination: 'KIAH' },
  operationalStatus: 'NORMAL',
  deviationType: 'NONE',
  telemetry: { fuelRemainingMin: 120, altitude: 35000 },
  aiAnalysis: {
    summaryTitle: 'On track',
    rootCause: 'None',
    downstreamImpact: 'None',
    recommendedAction: 'None',
  },
};

describe('FlightCard', () => {
  it('renders with status-normal class for NORMAL operationalStatus', () => {
    render(<FlightCard flight={{ ...base, operationalStatus: 'NORMAL' }} />);
    expect(screen.getByRole('article')).toHaveClass('status-normal');
  });

  it('renders with status-warning class for WARNING operationalStatus', () => {
    render(<FlightCard flight={{ ...base, operationalStatus: 'WARNING' }} />);
    expect(screen.getByRole('article')).toHaveClass('status-warning');
  });

  it('renders with status-critical class for CRITICAL operationalStatus', () => {
    render(<FlightCard flight={{ ...base, operationalStatus: 'CRITICAL' }} />);
    expect(screen.getByRole('article')).toHaveClass('status-critical');
  });

  it('displays the flight ID', () => {
    render(<FlightCard flight={base} />);
    expect(screen.getByText('AA123')).toBeInTheDocument();
  });

  it('displays the aircraft type', () => {
    render(<FlightCard flight={base} />);
    expect(screen.getByText('B737')).toBeInTheDocument();
  });

  it('displays the destination ICAO', () => {
    render(<FlightCard flight={base} />);
    expect(screen.getByText('KIAH')).toBeInTheDocument();
  });
});
