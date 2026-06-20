# FlightAware TV — Sprint Board

> Maintained by the Archivist Agent. Run `/sync-todo` after every merge to keep this current.
> Last updated: 2026-06-19

---

## Sprint 1 — MVP Core

**Goal:** Working end-to-end loop: SSE stream → multi-agent AI analysis → visual triage UI.
**Window:** 2026-06-08 → 2026-06-14 (closed)

### Done

- [x] Bootstrap monorepo (pyproject.toml, directory layout, CI scaffold)
- [x] Wire pre-commit hooks and developer setup docs
- [x] Define `FlightState` data contract (`backend/models/flight.py` + `frontend/src/types/flight.ts`)
- [x] Scaffold agent modules (`coordinator.py`, `route_analytics.py`, `crew_logistics.py`)
- [x] Set up Claude Code skills (`.claude/commands/`)
- [x] Implement `RouteAnalyticsAgent.analyze()` — telemetry anomaly detection against mock weather/runway data
- [x] Implement `CrewLogisticsAgent.assess()` — duty time limit + gate constraint computation
- [x] Implement `CoordinatorAgent.analyze()` — delegates to Route + Crew, validates output against `FlightState`
- [x] Wire `CoordinatorAgent` into `/api/fleet/stream` SSE endpoint (replace static mock)
- [x] Integrate Instructor + Gemini for structured AI analysis inside `CoordinatorAgent`
- [x] Add structured logging: elapsed_ms per flight enrichment per SSE cycle
- [x] Make CORS origins configurable via `CORS_ORIGINS` env var
- [x] Add `.env.example` — `GOOGLE_API_KEY` and `CORS_ORIGINS` placeholders
- [x] `GH_TOKEN` and `SLACK_WEBHOOK_URL` secrets configured in GitHub repository settings
- [x] Branch protection on `main` (1 approval required + CI checks green + enforce_admins)
- [x] `lhci autorun` passing in CI (Lighthouse accessibility gate ≥ 95)
- [x] `FlightCard` component — `status-normal/warning/critical` CSS class + left border, Vitest tests for all three states
- [x] `MockFlightBoard` — 3-column grid (IDENT/TYPE/TO), 25 mock flights, severity sort (CRITICAL → WARNING → NORMAL)
- [x] `sortFlightsBySeverity<T extends FlightState>()` generic sort utility (`src/utils/sortFlights.ts`)
- [x] `MapPanel` — MapLibre GL JS, vector tiles, 45 mock JFK aircraft, 30s position animation, hover tooltips
- [x] `AppLayout` — responsive shell: 60/40 desktop split, mobile tab bar, live clock

---

## Sprint 2 — SSE Wiring & Live Data

**Goal:** Replace all mock data with live `/api/fleet/stream` SSE feed; add `AiImpactDrawer`; close open issues.
**Window:** 2026-06-18 → 2026-06-19

### Karl — Backend

- [x] Derive expected flight IDs in `test_sse_payload_contains_all_flights` from `generate_mock_fleet()` rather than hardcoding `{"AA123", "UA456", "DL789", "SW202"}`
- [x] SSE throughput baseline — `scripts/perf_baseline.py` (~4ms/cycle, 277µs TTFE, 1600 enrichments/s at 10 connections)

### Ahsan — Frontend

- [x] Remove unused `leaflet`, `react-leaflet`, `@types/leaflet` from `package.json`
- [x] Remove `void positions` useState hack in `MapPanel.tsx` — replaced with `useRef`
- [x] Add `MapPanel` smoke test (`data-testid="map-panel"`)
- [x] Add `sortFlightsBySeverity` unit tests (sort order, immutability, stable ordering)
- [x] Escape `flightId`, `aircraftType`, route fields before passing to MapLibre `setHTML()` — XSS closed
- [x] Remove Tailwind — CSS custom properties are the single source of truth
- [x] Trim `sortFlightsBySeverity` docstring to one line
- [x] Implement `useFleetStream` hook — SSE client typed to `FlightState[]`, `isFlightState()` type guard (all 7 fields), `error` boolean, empty-array guard, EventSource cleanup
- [x] Wire `useFleetStream` into `AppLayout` (one connection serves both panels); `FlightsPanel` consumes live data
- [x] Map markers colored by live `operationalStatus`; `aiAnalysis.summaryTitle` in hover tooltips (positions remain mocked — see Sprint 3)
- [x] Loading skeleton ("Connecting to live feed…"), error state ("Feed disconnected — contact operations"), empty state ("No active disruptions")
- [x] `AiImpactDrawer` — slide-out panel on flight row click; renders all four `aiAnalysis` fields; accent color tracks `operationalStatus`; closes on X / Escape / backdrop; `role="dialog"` `aria-modal`
- [x] `MockFlightBoard` rows keyboard-accessible (`role=button`, `tabIndex=0`, Enter key)
- [x] `MockEventSource` stub gains `dispatch(data)` for future SSE data-path tests
- [x] `MapPanel` container ref replaces hardcoded `id="jfk-map"` — component is now composable

**Status: PR #42 open, CI green, awaiting Karl's re-review after addressing his requested changes.**

### E2e (blocked on PR #42 merge → fresh branch)

- [ ] Configure Playwright to run against a local backend stub for e2e isolation
- [ ] Write Playwright e2e: FBO operator sees `CRITICAL` flight sorted to top of queue
- [ ] Write Playwright e2e: clicking a `FlightCard` opens `AiImpactDrawer` with AI fields populated

---

## Sprint 3 — Hardening & Polish

**Goal:** Production-grade reliability, real map positions, accessibility certification.
**Window:** TBD (after Sprint 2 merges)

### Karl — Backend

- [ ] Add `lat`, `lon`, `heading` to `FlightState.telemetry` (Pydantic model + `simulation.py`) — required for real aircraft positions on the map; coordinate with Ahsan before touching the model

### Ahsan — Frontend

- [ ] Wire real `FlightState` lat/lon/heading into `MapPanel` — replace `JFKAircraft` mock positions once Karl ships the contract extension
- [ ] Accessibility pass — `axe-core` local run + confirm Lighthouse score ≥ 95 with live data flowing

### Shared / Infra

- [ ] Animate `AiImpactDrawer` open/close without layout shift (CSS `@keyframes` slide-in exists; layout shift under scroll not yet verified)

---

## Icebox

- [ ] Real-world telemetry adapter (AeroAPI requires paid access; OpenSky Network is a free alternative)
- [x] `lru-cache` version audit — `5.1.1` and `11.5.1` coexist cleanly via npm deduplication; neither enters the browser bundle; no action needed
- [ ] Multi-tenant support (FBO operators scoped to their own facility)
- [ ] Mobile-responsive layout pass
