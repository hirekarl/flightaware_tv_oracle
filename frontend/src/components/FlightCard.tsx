import React from 'react';
import type { FlightState, OperationalStatus } from '../types/flight';

interface Props {
  flight: FlightState;
}

const STATUS_CLASS: Record<OperationalStatus, string> = {
  NORMAL: 'status-normal',
  WARNING: 'status-warning',
  CRITICAL: 'status-critical',
};

const STATUS_STYLE: Record<OperationalStatus, React.CSSProperties> = {
  NORMAL: { color: '#fff' },
  WARNING: { borderLeft: '4px solid #F5A623', paddingLeft: '8px', color: '#fff' },
  CRITICAL: { borderLeft: '4px solid #D0021B', paddingLeft: '8px', color: '#fff' },
};

export default function FlightCard({ flight }: Props) {
  const { operationalStatus, flightId } = flight;

  return (
    <article
      className={STATUS_CLASS[operationalStatus]}
      style={{ padding: '6px 12px', ...STATUS_STYLE[operationalStatus] }}
      data-status={operationalStatus}
    >
      <span
        style={operationalStatus === 'CRITICAL' ? { fontWeight: 'bold' } : undefined}
      >
        {flightId}
      </span>
    </article>
  );
}
