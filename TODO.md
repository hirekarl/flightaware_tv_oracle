# FlightAware TV — Sprint Board

> Maintained by the Archivist Agent. Run `/sync-todo` after every merge to keep this current.
> Last updated: 2026-06-08

---

## Sprint 1 — MVP Core

**Goal:** Working end-to-end loop: SSE stream → multi-agent AI analysis → visual triage UI.
**Window:** 2026-06-08 → 2026-06-14

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
- [x] Write `pytest` tests for all agent `analyze()` / `assess()` return shapes (47 tests total)
- [x] SSE integration tests: HTTP contract, event format, payload schema, NORMAL-bypass invariant
- [x] `.env.example` with `GOOGLE_API_KEY` and `CORS_ORIGINS` placeholders
- [x] `GH_TOKEN` secret configured in GitHub repository settings
- [x] Branch protection on `main` (1 approval required + 3 CI checks green + enforce_admins)

### Karl — Backend

Nothing outstanding for Sprint 1.

### Ahsan — Frontend

- [ ] Build `FlightCard` component — distinct visual states for `NORMAL`, `WARNING`, `CRITICAL`
- [ ] Build `FlightQueue` list — sort order: `CRITICAL` → `WARNING` → `NORMAL`
- [ ] Build `AiImpactDrawer` slide-out panel — renders `aiAnalysis` fields on card click
- [ ] Implement `useFleetStream` hook — SSE client consuming `/api/fleet/stream`
- [ ] Wire `useFleetStream` into `FlightQueue` for live updates
- [ ] Implement empty states: loading skeleton + "No active disruptions" fallback copy
- [ ] Write Vitest unit tests for `FlightCard` (all three status states)
- [ ] Write Playwright e2e: dispatcher sees `CRITICAL` flight sorted to top of queue

### Shared / Infra

- [ ] Configure Playwright to run against a local backend stub for e2e isolation

---

## Sprint 2 — Hardening & Polish

**Goal:** Production-grade reliability, design system, real data readiness.
**Window:** TBD (after Sprint 1 MVP ships)

### Backend

- [ ] Rate limiting on `/api/fleet/stream` (prevent client reconnect storms)
- [ ] Real-world telemetry adapter (swap mock data for AeroAPI or similar)

### Frontend

- [ ] Design system tokens — map `NORMAL` / `WARNING` / `CRITICAL` to CSS custom properties
- [ ] Accessibility pass — `axe-core` local run + confirm Lighthouse score ≥ 95
- [ ] Animate `AiImpactDrawer` open/close without layout shift

### Shared / Infra

- [ ] Performance baseline — measure and document SSE throughput under simulated load
- [ ] Add Dependabot config for automated dependency PRs

---

## Icebox

Items deferred until after Sprint 2 or contingent on external factors.

- [ ] Real AeroAPI integration (requires paid API access)
- [ ] Multi-tenant support (dispatchers scoped to their own airline fleet)
- [ ] Mobile-responsive layout pass
