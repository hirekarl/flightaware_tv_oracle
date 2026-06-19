import { useEffect } from 'react';
import type { FlightState, OperationalStatus } from '../types/flight';

interface Props {
  flight: FlightState | null;
  onClose: () => void;
}

const STATUS_COLOR: Record<OperationalStatus, string> = {
  CRITICAL: '#D0021B',
  WARNING: '#F5A623',
  NORMAL: '#00A0E2',
};

const SLIDE_IN = `
@keyframes fa-slide-in {
  from { transform: translateX(100%); }
  to   { transform: translateX(0); }
}
`;

interface FieldProps {
  label: string;
  value: string;
  accent?: string;
  highlight?: boolean;
}

function Field({ label, value, accent, highlight }: FieldProps) {
  return (
    <div>
      <div
        style={{
          fontSize: '0.65rem',
          letterSpacing: '0.1em',
          color: accent ?? '#8fa8c8',
          fontWeight: 700,
          marginBottom: '6px',
          textTransform: 'uppercase',
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: '0.9rem',
          color: highlight ? 'var(--fa-blue)' : '#fff',
          lineHeight: 1.5,
          fontFamily: highlight ? 'monospace' : undefined,
          background: highlight ? 'rgba(0,160,226,0.08)' : undefined,
          borderLeft: highlight ? '2px solid var(--fa-blue)' : undefined,
          padding: highlight ? '8px 12px' : undefined,
          borderRadius: highlight ? '2px' : undefined,
        }}
      >
        {value}
      </div>
    </div>
  );
}

export default function AiImpactDrawer({ flight, onClose }: Props) {
  useEffect(() => {
    if (!flight) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [flight, onClose]);

  if (!flight) return null;

  const accent = STATUS_COLOR[flight.operationalStatus];

  return (
    <>
      <style>{SLIDE_IN}</style>
      {/* Backdrop */}
      <div
        aria-hidden="true"
        onClick={onClose}
        style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0,0,0,0.5)',
          zIndex: 99,
        }}
      />
      {/* Panel */}
      <aside
        role="dialog"
        aria-modal="true"
        aria-label={`AI analysis for ${flight.flightId}`}
        style={{
          position: 'fixed',
          top: 0,
          right: 0,
          bottom: 0,
          width: 'min(400px, 100vw)',
          background: 'var(--fa-navy)',
          borderLeft: `2px solid ${accent}`,
          zIndex: 100,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          animation: 'fa-slide-in 0.2s ease',
        }}
      >
        {/* Header */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            padding: '16px 20px',
            borderBottom: `1px solid ${accent}`,
            flexShrink: 0,
          }}
        >
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span
                style={{
                  fontFamily: 'monospace',
                  fontSize: '1.1rem',
                  fontWeight: 700,
                  color: '#fff',
                }}
              >
                {flight.flightId}
              </span>
              <span
                style={{
                  fontSize: '0.65rem',
                  fontWeight: 700,
                  letterSpacing: '0.08em',
                  color: accent,
                  border: `1px solid ${accent}`,
                  borderRadius: '3px',
                  padding: '1px 6px',
                }}
              >
                {flight.operationalStatus}
              </span>
            </div>
            <div style={{ color: '#8fa8c8', fontSize: '0.75rem', marginTop: '4px' }}>
              {flight.route.departure} → {flight.route.destination} ·{' '}
              {flight.aircraftType}
            </div>
          </div>
          <button
            onClick={onClose}
            aria-label="Close AI analysis panel"
            style={{
              background: 'transparent',
              border: '1px solid #2A3E6B',
              color: '#8fa8c8',
              cursor: 'pointer',
              borderRadius: '4px',
              padding: '4px 10px',
              fontSize: '1rem',
              lineHeight: 1,
              flexShrink: 0,
            }}
          >
            ✕
          </button>
        </div>

        {/* AI fields */}
        <div
          style={{
            padding: '20px',
            display: 'flex',
            flexDirection: 'column',
            gap: '20px',
          }}
        >
          <Field
            label="Situation"
            value={flight.aiAnalysis.summaryTitle}
            accent={accent}
          />
          <Field label="Root Cause" value={flight.aiAnalysis.rootCause} />
          <Field label="Downstream Impact" value={flight.aiAnalysis.downstreamImpact} />
          <Field
            label="Recommended Action"
            value={flight.aiAnalysis.recommendedAction}
            highlight
          />
        </div>
      </aside>
    </>
  );
}
