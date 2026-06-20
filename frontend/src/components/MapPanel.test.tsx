import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import MapPanel from './MapPanel';

describe('MapPanel', () => {
  it('renders without throwing and exposes data-testid', () => {
    render(<MapPanel />);
    expect(screen.getByTestId('map-panel')).toBeInTheDocument();
  });
});
