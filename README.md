# FlightAware TV — AI Fleet Disruption Oracle

Real-time airline operations dashboard that transforms reactive flight telemetry into predictive,
AI-driven action plans for fleet dispatchers.

## Repository Layout

```
flightaware_tv_oracle/
├── backend/              # Python 3.12 FastAPI application (the `backend` package)
│   ├── agents/           # Multi-agent orchestration: Coordinator, Route, Crew
│   └── models/           # Pydantic v2 data contract models
├── frontend/             # React 19 + Vite + TypeScript
│   └── src/
│       └── types/        # TypeScript interfaces (mirrors Pydantic models)
├── tests/                # pytest test suite
├── .github/workflows/    # CI pipeline
├── render.yaml           # Render Blueprint (free-tier API + static site)
├── pyproject.toml        # Python backend config (uv, ruff, mypy, pytest, semantic-release)
└── package.json          # Root: Husky + commitlint only
```

## Developer Setup

> **First time on this machine?** See [`docs/contributor-setup.md`](docs/contributor-setup.md)
> for full environment setup, Python installation via `uv`, GitHub CLI SSL troubleshooting,
> and browser-based authentication.

### Prerequisites

- **uv** — Python package manager
  - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Node.js 20+** with npm

### First-time setup (run once after cloning)

```bash
# Python environment + all dependencies (backend + dev tools)
uv sync --all-groups

# Root Node deps — installs Husky git hooks and commitlint
npm install

# Frontend deps
cd frontend && npm install && cd ..

# Download pre-commit hook environments (one-time, requires network)
uv run pre-commit install-hooks

# Copy the environment template and fill in your API key
cp .env.example .env
```

### Running the dev servers

Open two terminals from the repo root:

```bash
# Terminal 1 — backend
uv run uvicorn backend.main:app --reload
# → http://localhost:8000

# Terminal 2 — frontend
cd frontend && npm run dev
# → http://localhost:5173
```

## Data Contract

All telemetry flows through a single validated schema. The backend enforces it with Pydantic v2;
the frontend enforces it with TypeScript strict interfaces.

- Source of truth: `backend/models/flight.py` (`FlightState`)
- Frontend mirror: `frontend/src/types/flight.ts`

```json
{
  "flightId": "AA123",
  "aircraftType": "B738",
  "route": { "departure": "KJFK", "destination": "KORD" },
  "operationalStatus": "CRITICAL",
  "deviationType": "GO_AROUND",
  "telemetry": { "fuelRemainingMin": 45, "altitude": 2400 },
  "aiAnalysis": {
    "summaryTitle": "JFK Runway 22L Aborted Landing",
    "rootCause": "Windshear alert triggered at decision height.",
    "downstreamImpact": "High risk of crew timeout. Flight hits fuel reserves in 25 min.",
    "recommendedAction": "Divert immediately to KMKE (Milwaukee); gate K4 is open."
  }
}
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service liveness check |
| GET | `/api/fleet` | Snapshot of current fleet states |
| GET | `/api/fleet/stream` | SSE stream of live fleet updates (5s interval) |

## Testing

```bash
# Backend
uv run pytest

# Frontend unit + component
cd frontend && npm run test:unit

# Frontend e2e (Playwright)
cd frontend && npm run test:e2e

# Accessibility audit (Lighthouse CI)
lhci autorun
```

## Deployment

The project deploys via a [Render Blueprint](render.yaml) — connect the repo in the Render dashboard
and it provisions both services automatically.

| Service | Plan | URL |
|---|---|---|
| API (`flightaware-tv-oracle-api`) | Free web service | `https://flightaware-tv-oracle-api.onrender.com` |
| Frontend (`flightaware-tv-oracle`) | Free static site | `https://flightaware-tv-oracle.onrender.com` |

**First deploy:** Render will prompt for `GOOGLE_API_KEY` — have it ready.
**Free-tier caveat:** the API spins down after 15 min of inactivity; the first SSE connection to a
cold instance takes ~1 min to wake. Use a paid plan for production.

## Claude Code Skills

Project-level slash commands available in any Claude Code session. Skills live in `.claude/commands/`.

Code agents follow a TDD cycle: `/orchestrate` writes failing tests first; `/backend` and
`/frontend` implement only what is needed to pass them; `/qa` owns e2e coverage.

| Skill | Usage | What it does |
|---|---|---|
| `/orchestrate` | `/orchestrate <feature>` | TDD entry point — writes failing tests, confirms red, hands off to code agent |
| `/backend` | `/backend <task>` | Backend Core Agent — reads failing tests, implements to green, runs mypy |
| `/frontend` | `/frontend <task>` | Frontend UX Agent — reads failing tests, implements to green, runs Vitest |
| `/qa` | `/qa <task>` | QA Agent — Playwright e2e tests, axe-core injection, full suite verification |
| `/docs-sync` | `/docs-sync <task>` | Archivist Agent: documentation and knowledge base maintenance |
| `/validate` | `/validate` | Runs ruff → mypy → pytest → tsc → vitest; reports pass/fail per check |
| `/contract-check` | `/contract-check` | Diffs `FlightState` Pydantic model against TypeScript interfaces; flags drift |
| `/sync-todo` | `/sync-todo` | Rewrites `TODO.md` from `git log` + codebase structure |
| `/kb-update` | `/kb-update <url>` | Fetches a URL and synthesizes it into the matching `.knowledge_base/` leaf |

## CI/CD Pipeline

GitHub Actions validates every push and PR to `main` / `develop`:

1. **backend-validation** — ruff check, ruff format, mypy strict, pytest
2. **frontend-validation** — ESLint, tsc, vitest, playwright
3. **accessibility-audit** — Lighthouse CI (asserts accessibility ≥ 95)
4. **automated-release** *(merge to main only)* — python-semantic-release: version bump,
   CHANGELOG.md update, GitHub Release tag

## Branch Protocol

| Prefix | Use |
|---|---|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation updates |
| `ci/` | Pipeline changes |

- Never commit directly to `main`
- Every PR requires one human approval + all CI checks green
- Merge strategy: **Squash and Merge** (required for semantic-release linear history)

## Environment Variables

Copy `.env.example` to `.env` and fill in required values before running the backend.

```bash
cp .env.example .env
```
