import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AppLayout from './AppLayout';

function mockMatchMedia(isMobile: boolean) {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches: isMobile,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
}

describe('AppLayout — desktop (≥ 1024px)', () => {
  beforeEach(() => mockMatchMedia(false));

  it('renders the map panel', () => {
    render(<AppLayout />);
    expect(screen.getByTestId('map-panel')).toBeInTheDocument();
  });

  it('renders the flights panel', () => {
    render(<AppLayout />);
    expect(screen.getByTestId('flights-panel')).toBeInTheDocument();
  });

  it('does not render a tab bar on desktop', () => {
    render(<AppLayout />);
    expect(screen.queryByRole('tablist')).not.toBeInTheDocument();
  });
});

describe('AppLayout — mobile (< 1024px)', () => {
  beforeEach(() => mockMatchMedia(true));

  it('renders a tab bar with Map and Flights tabs', () => {
    render(<AppLayout />);
    expect(screen.getByRole('tablist')).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /map/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /flights/i })).toBeInTheDocument();
  });

  it('shows the map panel by default on mobile', () => {
    render(<AppLayout />);
    expect(screen.getByTestId('map-panel')).toBeInTheDocument();
    expect(screen.queryByTestId('flights-panel')).not.toBeInTheDocument();
  });

  it('switches to the flights panel when the Flights tab is clicked', async () => {
    const user = userEvent.setup();
    render(<AppLayout />);
    await user.click(screen.getByRole('tab', { name: /flights/i }));
    expect(screen.getByTestId('flights-panel')).toBeInTheDocument();
    expect(screen.queryByTestId('map-panel')).not.toBeInTheDocument();
  });

  it('marks the active tab with aria-selected="true"', async () => {
    const user = userEvent.setup();
    render(<AppLayout />);
    expect(screen.getByRole('tab', { name: /map/i })).toHaveAttribute(
      'aria-selected',
      'true'
    );
    await user.click(screen.getByRole('tab', { name: /flights/i }));
    expect(screen.getByRole('tab', { name: /flights/i })).toHaveAttribute(
      'aria-selected',
      'true'
    );
  });
});
