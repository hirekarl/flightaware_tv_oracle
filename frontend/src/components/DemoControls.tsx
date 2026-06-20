import { useState, useEffect } from 'react';

const API_URL =
  (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000';

interface BeatState {
  beat: number;
  name: string;
}

const TOTAL_BEATS = 6;

export default function DemoControls() {
  const [state, setState] = useState<BeatState>({ beat: 0, name: '…' });
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/demo/status`)
      .then((r) => r.json())
      .then((d: BeatState) => setState(d))
      .catch(() => undefined);
  }, []);

  async function post(path: string) {
    if (busy) return;
    setBusy(true);
    try {
      const r = await fetch(`${API_URL}${path}`, { method: 'POST' });
      const d: BeatState = await r.json();
      setState(d);
    } catch {
      // ignore — board still reflects last known beat
    } finally {
      setBusy(false);
    }
  }

  return (
    <div
      role="toolbar"
      aria-label="Demo controls"
      style={{
        position: 'fixed',
        bottom: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        padding: '8px 16px',
        background: 'rgba(6,35,64,0.95)',
        border: '1px solid #2A3E6B',
        borderRadius: 999,
        boxShadow: '0 4px 24px rgba(0,0,0,0.5)',
        backdropFilter: 'blur(8px)',
        color: '#fff',
        fontSize: '0.8rem',
        whiteSpace: 'nowrap',
        userSelect: 'none',
      }}
    >
      <span style={{ color: '#00a0e2', fontWeight: 700, letterSpacing: '0.04em' }}>
        DEMO
      </span>
      <span style={{ color: '#8fa8c8' }}>
        Beat {state.beat + 1}/{TOTAL_BEATS} · {state.name}
      </span>
      <button
        onClick={() => post('/demo/next')}
        disabled={busy}
        aria-label="Advance to next beat"
        style={{
          padding: '4px 14px',
          background: '#00a0e2',
          border: 'none',
          borderRadius: 999,
          color: '#fff',
          fontWeight: 700,
          fontSize: '0.8rem',
          cursor: busy ? 'not-allowed' : 'pointer',
          opacity: busy ? 0.6 : 1,
        }}
      >
        Next Beat →
      </button>
      <button
        onClick={() => post('/demo/reset')}
        disabled={busy}
        aria-label="Reset to beat 0"
        style={{
          padding: '4px 10px',
          background: 'transparent',
          border: '1px solid #2A3E6B',
          borderRadius: 999,
          color: '#8fa8c8',
          fontSize: '0.8rem',
          cursor: busy ? 'not-allowed' : 'pointer',
          opacity: busy ? 0.6 : 1,
        }}
      >
        ↺ Reset
      </button>
    </div>
  );
}
