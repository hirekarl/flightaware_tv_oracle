# FlightAware TV Oracle — Demo Script

**Runtime:** ~4 minutes
**Speakers:** Karl (backend / architecture) · Ahsan (frontend / UX)
**Setup:** Both servers running. Open `http://localhost:5173?demo=true`. Board at Beat 0.

Advance **→ Next Beat** 1–2 seconds *before* speaking the corresponding line.
The SSE stream refreshes within 5 seconds of each advance.

---

## Act 1 — Problem & Project Context (Karl, ~30s)

Fixed-base operators run the ground side of aviation: fueling, ramp handling, crew
services, gate coordination. When a weather system closes a runway or a flight declares
minimum fuel, an FBO can get five unplanned aircraft on the ramp in under an hour — each
one needing fuel trucks, ground crew, and gate clearance simultaneously.

FlightAware TV is a live flight display product built for airports and lounges — it shows
you what's in the air. We took that model and rebuilt the backend for FBO operators:
instead of showing flight status, the system tells you which aircraft are heading your way,
why, and what they'll need on the ground before they land.

Every flight on this board is being analyzed continuously by a multi-agent AI pipeline
backed by Gemini. The operator sees severity-sorted triage and one-click action briefs —
not a flat list of status codes.

---

## Act 2 — Architecture (Ahsan, ~30s)

The foundation is a strict data contract: a Pydantic v2 `FlightState` model on the backend
mirrored as TypeScript strict interfaces on the frontend — no `any`, both sides validated at
every boundary. When the schema changes, both sides agree before any feature code is written.

Transport is SSE — Server-Sent Events. The backend streams a full fleet snapshot every five
seconds over a persistent HTTP connection. The frontend's `useFleetStream` hook opens that
connection on mount, validates every payload, and updates the board. If the connection
drops, the board shows "Feed disconnected" in red.

---

## Act 3 — Live Demo (both, ~2 min)

*Board is at Beat 0.*

**Karl:** Beat zero — normal JFK morning. AA123 is cruising, two background disruptions
already in progress. The AI is generating analysis on both; click either to see it.

*Advance → Beat 1.*

**Ahsan:** AA123 enters a holding pattern over JFK. Fuel is at 110 minutes — amber, but
manageable. The board sorted it above SW202 automatically. Severity-first ordering is baked
into the sort utility.

*Advance → Beat 2.*

**Karl:** AA123 missed the approach — that's a go-around, 85 minutes of fuel at 2,500
feet. SW202 cleared in the same cycle. The system tracks resolutions in real time alongside
escalations.

*Advance → Beat 3.*

**Ahsan:** Two reds. UA456 diverted, AA123 still critical in the go-around. Click AA123.

*Click to open AiImpactDrawer.*

Four structured fields: situation summary, root cause, downstream impact, and recommended
action — generated live by Gemini and validated against the data contract before they reach
the screen. Everything the FBO operator needs to start coordinating ramp resources before
the aircraft even lands.

*Close drawer. Advance → Beat 4.*

**Karl:** AA123 diverts to its alternate. NK501 just went critical in the hold — 38 minutes
of fuel. The system caught that before the crew called it in. DL789 picks up a hold too.
The board is showing you the cascade as it develops.

*Advance → Beat 5.*

**Ahsan:** AA123 and UA456 landed at their alternates — both back to green on the next SSE
cycle. NK501 is still critical at 28 minutes. The board tells you exactly where to
pre-position fuel trucks.

---

## Act 4 — Challenges & Close (both, ~1 min)

**Karl:** The hardest backend problem was structured LLM output at SSE speed. We run 15
concurrent Gemini calls per cycle via `asyncio.gather`. We benchmarked at 4 milliseconds
per cycle excluding LLM latency, with headroom for 10 simultaneous operator connections.
SSE over WebSockets was a deliberate call: unidirectional, plain HTTP, no reconnection
protocol, compatible with every CDN without configuration.

**Ahsan:** On the frontend, the type guard in `useFleetStream` validates all seven required
fields on every incoming payload. Malformed output gets discarded before it touches the
board. The accessibility gate — Lighthouse CI at 95 on every PR — pushed us to make the
flight board fully keyboard-navigable since the WebGL map can't be made accessible.

**Karl:** Swap `generate_mock_fleet()` for a live AeroAPI feed and the pipeline runs
unchanged. Happy to go deeper on any of the engineering choices.

---

## Beat Advance Cheat Sheet

| Cue | Action |
|---|---|
| "opens on a normal JFK morning" | Already at Beat 0 — no advance |
| "AA123 enters a holding pattern" | Advance → Beat 1 |
| "AA123 missed the approach" | Advance → Beat 2 |
| "Two reds. UA456 diverted" | Advance → Beat 3 |
| "AA123 diverts to its alternate" | Advance → Beat 4 |
| "AA123 and UA456 landed" | Advance → Beat 5 |
