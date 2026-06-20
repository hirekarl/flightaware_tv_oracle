# FlightAware TV Oracle — Demo Script

**Runtime:** ~4 minutes
**Speakers:** Karl (backend / AI) · Ahsan (frontend / UX)
**Setup:** Both servers running. Open `http://localhost:5173?demo=true`. Board at Beat 1.

Advance **→ Next Beat** 1–2 seconds *before* speaking the corresponding line.
The board updates within 5 seconds of each advance.

---

## Act 1 — Problem & Context (Karl, ~30s)

Fixed-base operators handle aviation's ground side: fueling, ramp crews, gate
coordination. When weather shuts a runway, five unplanned aircraft can arrive on your
ramp in under an hour.

Business aviation clients pay premium rates for anticipatory service. One missed handoff
when a $60 million G650 pulls up can cost an FBO $5 million in annual revenue.

Last week we built the display. This week we made it predictive.

---

## Act 2 — What We Built This Week (Ahsan, ~30s)

Week 1 was the real-time feed — aircraft status streaming to the board every five
seconds, severity-sorted automatically.

This week we added the AI layer: a Gemini-powered multi-agent pipeline that reads route
and crew data, then surfaces an action card per flight. Not just a problem — what to do
about it.

---

## Act 3 — Live Demo (both, ~2 min)

*Board is at Beat 1.*

**Karl:** Normal JFK morning. Twenty aircraft, two disruptions in progress. AI is running
on every flight. Click either amber card.

*Advance → Beat 2.*

**Ahsan:** AA123 is now in a holding pattern. A two-hour hold at this fuel level costs
the FBO $3,000 in ramp time. The board sorted it to the top — highest-stakes aircraft
first, always.

*Advance → Beat 3.*

**Karl:** AA123 missed its approach — go-around at 2,500 feet, 85 minutes of fuel.
SW202 cleared in the same cycle. The board tracks resolutions alongside escalations.

*Advance → Beat 4.*

**Ahsan:** Two reds. UA456 diverted, AA123 still critical. Click AA123.

*Click to open AiImpactDrawer.*

Situation, root cause, downstream impact, recommended action — generated live by Gemini.
An action brief, not a status code. The line manager knows what to do before the
aircraft lands.

*Close drawer. Advance → Beat 5.*

**Karl:** AA123 diverts. NK501 just went critical — 38 minutes of fuel in the hold.
The Oracle caught it before the crew called in. That's where FBOs earn or lose a client.

*Advance → Beat 6.*

**Ahsan:** AA123 and UA456 back to green. NK501 still critical at 28 minutes — the board
tells you where to pre-position fuel trucks and which gate to hold.

---

## Act 4 — Challenges & Close (both, ~1 min)

**Karl:** The hardest problem was speed. Fifteen concurrent Gemini calls per cycle, all
resolving before the board updates — the operator never waits for analysis. The pipeline
is built so you can swap in a different AI model without touching anything else.

**Ahsan:** The design challenge was density. FBO ops managers read this from across a
room while coordinating ground crews by radio. The action drawer is one click — always
available, never in the way.

**Karl:** A live AeroAPI feed is a trivial swap. The Oracle scales from a single FBO to
a regional network — and the goal stays the same: an ops manager never finds out about
a disruption after it's already cost them a client.

---

## Beat Advance Cheat Sheet

| Cue | Action |
|---|---|
| "Normal JFK morning" | Already at Beat 1 — no advance |
| "AA123 is now in a holding pattern" | Advance → Beat 2 |
| "AA123 missed its approach" | Advance → Beat 3 |
| "Two reds. UA456 diverted" | Advance → Beat 4 |
| "AA123 diverts" | Advance → Beat 5 |
| "AA123 and UA456 back to green" | Advance → Beat 6 |
