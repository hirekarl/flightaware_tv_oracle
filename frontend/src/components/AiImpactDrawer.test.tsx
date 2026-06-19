import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AiImpactDrawer from './AiImpactDrawer';
import type { FlightState } from '../types/flight';

const mockFlight: FlightState = {
  flightId: 'DL789',
  aircraftType: 'B788',
  route: { departure: 'KATL', destination: 'KORD' },
  operationalStatus: 'CRITICAL',
  deviationType: 'DIVERSION',
  telemetry: { fuelRemainingMin: 42, altitude: 31000 },
  aiAnalysis: {
    summaryTitle: 'Diverting to KMDW — low fuel',
    rootCause: 'Unanticipated headwinds consumed reserve',
    downstreamImpact: '3 connecting flights at risk',
    recommendedAction: 'Declare minimum fuel, coordinate KMDW crew',
  },
};

describe('AiImpactDrawer', () => {
  it('renders nothing when flight is null', () => {
    const { container } = render(<AiImpactDrawer flight={null} onClose={() => {}} />);
    expect(container).toBeEmptyDOMElement();
  });

  it('renders the flight ID and operational status when open', () => {
    render(<AiImpactDrawer flight={mockFlight} onClose={() => {}} />);
    expect(screen.getByText('DL789')).toBeInTheDocument();
    expect(screen.getByText('CRITICAL')).toBeInTheDocument();
  });

  it('renders all four AI analysis fields', () => {
    render(<AiImpactDrawer flight={mockFlight} onClose={() => {}} />);
    expect(screen.getByText('Diverting to KMDW — low fuel')).toBeInTheDocument();
    expect(
      screen.getByText('Unanticipated headwinds consumed reserve')
    ).toBeInTheDocument();
    expect(screen.getByText('3 connecting flights at risk')).toBeInTheDocument();
    expect(
      screen.getByText('Declare minimum fuel, coordinate KMDW crew')
    ).toBeInTheDocument();
  });

  it('calls onClose when the close button is clicked', async () => {
    const onClose = vi.fn();
    const user = userEvent.setup();
    render(<AiImpactDrawer flight={mockFlight} onClose={onClose} />);
    await user.click(screen.getByRole('button', { name: /close/i }));
    expect(onClose).toHaveBeenCalledOnce();
  });

  it('calls onClose when Escape is pressed', async () => {
    const onClose = vi.fn();
    const user = userEvent.setup();
    render(<AiImpactDrawer flight={mockFlight} onClose={onClose} />);
    await user.keyboard('{Escape}');
    expect(onClose).toHaveBeenCalledOnce();
  });

  it('exposes role="dialog" with aria-modal for accessibility', () => {
    render(<AiImpactDrawer flight={mockFlight} onClose={() => {}} />);
    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
  });
});
