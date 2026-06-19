import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MockFlightBoard from './MockFlightBoard';
import { mockFlights } from '../fixtures/mockFlights';

describe('MockFlightBoard', () => {
  it('renders a row for every flight in the list', () => {
    render(<MockFlightBoard flights={mockFlights} />);
    mockFlights.forEach((flight) => {
      expect(screen.getByText(flight.flightId)).toBeInTheDocument();
    });
  });

  it('renders the aircraft type (TYPE column) for each flight', () => {
    render(<MockFlightBoard flights={mockFlights} />);
    mockFlights.forEach((flight) => {
      expect(screen.getAllByText(flight.aircraftType).length).toBeGreaterThan(0);
    });
  });

  it('renders the destination ICAO for each flight', () => {
    render(<MockFlightBoard flights={mockFlights} />);
    mockFlights.forEach((flight) => {
      expect(screen.getAllByText(flight.route.destination).length).toBeGreaterThan(0);
    });
  });

  it('renders the departTime for each flight', () => {
    render(<MockFlightBoard flights={mockFlights} />);
    mockFlights.forEach((flight) => {
      expect(screen.getByText(flight.departTime)).toBeInTheDocument();
    });
  });

  it('renders column headers: IDENT, TYPE, TO, DEPART', () => {
    render(<MockFlightBoard flights={mockFlights} />);
    expect(screen.getByText('IDENT')).toBeInTheDocument();
    expect(screen.getByText('TYPE')).toBeInTheDocument();
    expect(screen.getByText('TO')).toBeInTheDocument();
    expect(screen.getByText('DEPART')).toBeInTheDocument();
  });

  it('renders an empty-state message when passed an empty array', () => {
    render(<MockFlightBoard flights={[]} />);
    expect(screen.getByText(/no flights/i)).toBeInTheDocument();
  });

  it('calls onFlightClick with the clicked flight', async () => {
    const onFlightClick = vi.fn();
    const user = userEvent.setup();
    render(<MockFlightBoard flights={mockFlights} onFlightClick={onFlightClick} />);
    await user.click(screen.getByText(mockFlights[0].flightId));
    expect(onFlightClick).toHaveBeenCalledWith(mockFlights[0]);
  });
});
