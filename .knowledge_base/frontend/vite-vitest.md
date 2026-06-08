# Vite + Vitest

**Versions:** `vite>=8.0` (current: 8.0.16), `vitest>=4.0` (current: 4.1.7)
**Role:** Vite is the build tool and dev server. Vitest is the unit/component test
runner configured inside `vite.config.ts` (shares the same transform pipeline).

---

## Key Patterns

### vite.config.ts structure
```typescript
/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': resolve(__dirname, './src') } },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
  },
});
```
The `/// <reference types="vitest" />` triple-slash directive unlocks the `test`
config block inside `defineConfig` without a separate `vitest.config.ts`.

### Writing a component test
```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import FlightCard from '../FlightCard';

describe('FlightCard', () => {
  it('renders CRITICAL status with correct visual class', () => {
    render(<FlightCard flight={mockCriticalFlight} />);
    expect(screen.getByRole('article')).toHaveClass('status-critical');
  });
});
```

### Running tests
```bash
npm run test:unit       # single run (CI)
npm run test:watch      # watch mode — only reruns tests affected by changed files
```
Vitest's watch mode mirrors Vite HMR — it only reruns tests related to changed
modules rather than the full suite.

### Path aliases in tests
The `@/` alias defined in `vite.config.ts` resolves automatically in test files —
no extra configuration needed.

---

## Gotchas

- Vitest is now at **v4** (not v2 as the bootstrapping doc assumed). The config API
  is stable but verify any v2→v4 differences if migrating existing tests.
- Vite is at **v8** (powered by Rolldown for production builds). The dev server and
  config surface are backwards-compatible with v6 patterns.
- `globals: true` in the test config makes `describe`, `it`, `expect` available
  without imports. If you prefer explicit imports, set `globals: false`.
- jsdom does not implement `EventSource` (the browser SSE API). Mock it in
  `src/test/setup.ts` or use `vi.stubGlobal('EventSource', MockEventSource)`.
- Coverage requires `@vitest/coverage-v8` as an additional dev dep — not bundled.
- `@vitejs/plugin-react` uses the React compiler transform in Vite 8. Fast Refresh
  still works; you do not need to configure Babel separately.

---

## Resources

- https://vitest.dev/ (Vitest homepage — fetched 2026-06-08, v4.1.7)
- https://vite.dev/ (Vite homepage — fetched 2026-06-08, v8.0.16)
<!-- Drop additional links here — Archivist will synthesize -->
