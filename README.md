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
├── pyproject.toml        # Python backend config (uv, ruff, mypy, pytest, semantic-release)
└── package.json          # Root: Husky + commitlint only
```

## Quick Start

**Backend**

```bash
uv sync --group dev
uv run uvicorn backend.main:app --reload
# → http://localhost:8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
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
