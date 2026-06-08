# TypeScript (strict)

**Version:** `typescript>=6.0` (TypeScript 6.0 now available as of 2026-06-08)
**Role:** Static type safety across the frontend. All data contract types are
immutable interfaces mirroring the Pydantic backend models. `strict: true` enforces
the full suite of checks.

---

## Key Patterns

### Data contract interfaces (immutable)
```typescript
export interface FlightState {
  readonly flightId: string;
  readonly operationalStatus: 'NORMAL' | 'WARNING' | 'CRITICAL';
  readonly aiAnalysis: AiAnalysis;
  // ...
}
```
`readonly` on every field matches Pydantic `frozen=True` intent and prevents
accidental mutation in components.

### Narrowing operational status exhaustively
```typescript
function getStatusClass(status: OperationalStatus): string {
  const map: Record<OperationalStatus, string> = {
    NORMAL: 'status-normal',
    WARNING: 'status-warning',
    CRITICAL: 'status-critical',
  };
  return map[status];
}
```
`Record<OperationalStatus, string>` errors if a new union member is added without
updating the map — compile-time exhaustiveness check without a `switch`.

### Type-guarding SSE payloads at the boundary
```typescript
function isFlightState(value: unknown): value is FlightState {
  return (
    typeof value === 'object' &&
    value !== null &&
    'flightId' in value &&
    'operationalStatus' in value
  );
}

function parseFleetEvent(raw: string): FlightState[] {
  const parsed: unknown = JSON.parse(raw);
  if (!Array.isArray(parsed)) return [];
  return parsed.filter(isFlightState);
}
```
Never cast `unknown` SSE data directly with `as FlightState[]` — guard it first.

### Type-only imports (keeps bundle clean)
```typescript
import type { FlightState, AiAnalysis } from '@/types/flight';
```

### tsconfig.json key flags
```json
{
  "strict": true,           // enables the full strict suite
  "noImplicitAny": true,    // no implicit any types
  "strictNullChecks": true, // null/undefined must be handled explicitly
  "noUnusedLocals": true,   // dead locals fail the build
  "noUnusedParameters": true
}
```

---

## Gotchas

- **TypeScript 6.0** is the current stable version. Our `tsconfig.json` targets
  `ES2022` — verify any TS6 breaking changes against existing config before running
  `npm install`.
- `noUnusedLocals` and `noUnusedParameters` fail the build on dead code. Prefix
  intentionally unused params with `_` (e.g., `_event`).
- `allowImportingTsExtensions: true` is required by Vite + Vitest. It forces
  `noEmit: true` — TypeScript won't emit JS with this flag active.
- `moduleResolution: "bundler"` is correct for Vite but breaks `tsc` when
  `noEmit: false`. Keep `noEmit: true`.
- **Never use `any`** — if you receive `unknown` data (SSE, API response), use a
  type guard or runtime validator to narrow it before use.
- The `@/` path alias maps to `src/`. Use it consistently to avoid fragile relative
  import chains across the component tree.

---

## Resources

- https://www.typescriptlang.org/ (TypeScript homepage, v6.0 — fetched 2026-06-08)
