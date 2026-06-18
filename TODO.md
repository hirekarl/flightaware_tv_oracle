# FlightAware TV — Sprint Board

> Maintained by the Archivist Agent. Run `/sync-todo` after every merge to keep this current.
> Last updated: 2026-06-18

---

## Sprint 1 — MVP Core

**Goal:** Working end-to-end loop: SSE stream → multi-agent AI analysis → visual triage UI.
**Window:** 2026-06-08 → 2026-06-14 (closed; frontend SSE wiring carried into Sprint 2)

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
- [x] `MockFlightBoard` — 4-column grid (IDENT/TYPE/TO/DEPART), 25 mock flights, severity sort (CRITICAL → WARNING → NORMAL)
- [x] `sortFlightsBySeverity<T extends FlightState>()` generic sort utility (`src/utils/sortFlights.ts`)
- [x] `MapPanel` — MapLibre GL JS, vector tiles, 45 mock JFK aircraft, 30s position animation, hover tooltips
- [x] `AppLayout` — responsive shell: 60/40 desktop split, mobile tab bar, live clock

---

## Sprint 2 — SSE Wiring & Live Data

**Goal:** Replace all mock data with live `/api/fleet/stream` SSE feed; add `AiImpactDrawer`; close open issues.
**Window:** 2026-06-18 → TBD

### Karl — Backend

- [ ] Derive expected flight IDs in `test_sse_payload_contains_all_flights` from `generate_mock_fleet()` rather than hardcoding `{"AA123", "UA456", "DL789", "SW202"}`

### Ahsan — Frontend

**Issue #29 — required before live wiring:**
- [ ] Remove unused `leaflet`, `react-leaflet`, `@types/leaflet` from `package.json` (replaced by MapLibre GL)
- [ ] Remove `void positions` hack in `MapPanel.tsx` — drop unused React state or put it to use
- [ ] Add `MapPanel` smoke test (`data-testid="map-panel"` present, renders without throwing)
- [ ] Add `sortFlightsBySeverity` unit test (CRITICAL → WARNING → NORMAL order is load-bearing)
- [ ] Escape `flightId`, `aircraftType`, route fields before passing to MapLibre `setHTML()` — XSS risk once live `FlightState` is wired in

**Issue #27 — housekeeping:**
- [ ] Decide: migrate components to Tailwind utility classes OR remove Tailwind and own the CSS custom property approach — leaving both is dead weight
- [ ] Trim `sortFlightsBySeverity` docstring (narrates the code; drop or reduce to one non-obvious line)

**SSE wiring:**
- [ ] Implement `useFleetStream` hook — SSE client consuming `/api/fleet/stream`, typed to `FlightState[]`
- [ ] Wire `useFleetStream` into `MockFlightBoard` — replace `mockFlights` fixture with live data
- [ ] Replace `JFKAircraft` mock in `MapPanel.tsx` with live `FlightState` telemetry (position from `telemetry`, status color from `operationalStatus`)
- [ ] Implement empty states: loading skeleton while SSE connects + "No active disruptions" fallback when queue is empty
- [ ] Build `AiImpactDrawer` slide-out panel — renders `aiAnalysis.summaryTitle`, `rootCause`, `downstreamImpact`, `recommendedAction` on `FlightCard` click

**E2e:**
- [ ] Configure Playwright to run against a local backend stub for e2e isolation
- [ ] Write Playwright e2e: dispatcher sees `CRITICAL` flight sorted to top of queue
- [ ] Write Playwright e2e: clicking a `FlightCard` opens `AiImpactDrawer` with AI fields populated

### Shared / Infra

- [ ] Performance baseline — measure and document SSE throughput under simulated load

---

## Sprint 3 — Hardening & Polish

**Goal:** Production-grade reliability, design system, accessibility certification.
**Window:** TBD (after Sprint 2 ships)

### Backend

- [ ] Real-world telemetry adapter (swap mock data for AeroAPI or similar)

### Frontend

- [ ] Animate `AiImpactDrawer` open/close without layout shift
- [ ] Accessibility pass — `axe-core` local run + confirm Lighthouse score ≥ 95 with live data

---

## Icebox

- [ ] Real AeroAPI integration (requires paid API access)
- [ ] Multi-tenant support (dispatchers scoped to their own airline fleet)
- [ ] Mobile-responsive layout pass
- [ ] `lru-cache` version audit — lock file downgrades from 11.5.1 → 5.1.1 via MapLibre transitive dep; assess if this causes issues
