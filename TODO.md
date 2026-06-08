# FlightAware TV — Sprint TODO

> Maintained by the Archivist Agent. Update on every PR merge to `main`.
> Last updated: 2026-06-08

---

## Karl — Backend

### In Progress
- [ ] Bootstrap monorepo structure (pyproject.toml, directory layout, CI scaffold)

### Up Next
- [ ] Implement `RouteAnalyticsAgent.analyze()` — telemetry anomaly detection against mock weather/runway data
- [ ] Implement `CrewLogisticsAgent.assess()` — duty time limit + gate constraint computation
- [ ] Implement `CoordinatorAgent.analyze()` — delegates to Route + Crew agents, validates output against `FlightState`
- [ ] Wire `CoordinatorAgent` into the `/api/fleet/stream` SSE endpoint (replace static mock)
- [ ] Integrate LangChain + OpenAI for AI analysis generation inside `CoordinatorAgent`
- [ ] Add structured logging: log forecast vs. actual simulation metrics per SSE cycle
- [ ] Write `pytest` tests for all agent `analyze()` / `assess()` return shapes
- [ ] Add `.env.example` with `OPENAI_API_KEY` placeholder and FastAPI CORS origin config

### Backlog
- [ ] Rate limiting on `/api/fleet/stream` (prevent client reconnect storms)
- [ ] Integration tests for the SSE endpoint (assert event format, connection lifecycle)
- [ ] Implement real-world telemetry adapter (swap mock data for AeroAPI or similar)

---

## Ahsan — Frontend

### In Progress
- [ ] Review data contract in `frontend/src/types/flight.ts`

### Up Next
- [ ] Build `FlightCard` component — distinct visual states for `NORMAL`, `WARNING`, `CRITICAL`
  (border tokens, background shifts; no third-party a11y overlays)
- [ ] Build `FlightQueue` list component — sort: `CRITICAL` → `WARNING` → `NORMAL`
- [ ] Build `AiImpactDrawer` slide-out panel — renders `aiAnalysis` fields on card click
- [ ] Implement `useFleetStream` hook — SSE client consuming `/api/fleet/stream`
- [ ] Wire `useFleetStream` into `FlightQueue` for live updates
- [ ] Implement intentional empty state: loading skeleton and "No active disruptions" copy
- [ ] Write Vitest unit tests for `FlightCard` (all three status states)
- [ ] Write Playwright e2e test: dispatcher sees `CRITICAL` flight sorted to top of queue

### Backlog
- [ ] Design system tokens — map `NORMAL` / `WARNING` / `CRITICAL` to CSS custom properties
- [ ] Accessibility pass — run `axe-core` locally and verify Lighthouse score ≥ 95
- [ ] Animate drawer open/close without layout shift

---

## Shared / Infra

- [ ] Enable GitHub branch protection on `main` (require PR approval + all CI checks)
- [ ] Add `GH_TOKEN` secret in GitHub repository settings (required for automated-release job)
- [ ] Verify `lhci autorun` passes locally before first PR to `main`
- [ ] Add `.env.example` to repo root
- [ ] Configure Playwright to run against a local backend stub for e2e isolation
