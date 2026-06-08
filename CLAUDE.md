# FlightAware TV — AI Fleet Disruption Oracle

## Project Overview

B2B operational dashboard for airline operations dispatchers. Transforms reactive flight telemetry into
predictive, AI-driven action plans via a high-density web UI backed by a FastAPI streaming API.

**Team:** Karl Johnson (backend), Ahsan Abbasi (frontend)
**Stack:** Python 3.12 (FastAPI + uv) / React 19 (Vite + TypeScript)
**Architecture:** Monorepo — `backend/` (Python package) and `frontend/` (React app) — decoupled via SSE + strict JSON data contract.

---

## CRITICAL: Commit Authorship

**Never** add `Co-authored-by:` lines attributing Claude, Anthropic, or any AI tool to git commits.
This project's history must reflect only human authors.

The `.husky/commit-msg` hook enforces this automatically by stripping those lines before commitlint
runs. Do not attempt to bypass the hook or re-add attribution after the fact.

---

## Data Contract

The canonical schema lives in `backend/models/flight.py` as `FlightState` (Pydantic v2).
The frontend mirrors it in `frontend/src/types/flight.ts` as immutable TypeScript interfaces.

**Rule:** Never pass raw `dict` where a typed `FlightState` (or sub-model) should exist. Backend
endpoints must return typed Pydantic models. Frontend components must accept typed `FlightState`
props — no `any`, no `unknown` without an explicit assertion.

---

## Toolchain

| Layer | Tool | Command |
|---|---|---|
| Python env | `uv` | All Python commands via `uv run` |
| Lint + format | `ruff` | Replaces black + isort |
| Type check | `mypy --strict` | `uv run mypy backend/ --strict` |
| Testing (backend) | `pytest` + `pytest-asyncio` | `uv run pytest` |
| Frontend build | Vite | `npm run build` (in `frontend/`) |
| Frontend testing | Vitest + Playwright | `npm run test:unit` / `npm run test:e2e` |
| Accessibility | axe-core + Lighthouse CI | Score gate ≥ 95 in CI |
| Versioning | `python-semantic-release` | Automated on merge to `main` |
| Changelogs | `commitizen` | `cz changelog` for local preview |
| Commit hooks | Husky + commitlint | Enforces Conventional Commits |

---

## Agent Roles

Invoke a skill to activate the relevant agent. The skill reads its knowledge base leaves
before generating any code or docs.

### Backend Core Agent — `backend/` · `/backend <task>`
FastAPI endpoints, Pydantic models, async event loops, SSE stream.
Reject any raw `dict` where a typed Pydantic model should exist.

### Frontend UX Agent — `frontend/` · `/frontend <task>`
React 19 components, SSE client hook, visual state (Normal / Warning / Critical).
No third-party accessibility overlay widgets. TypeScript interfaces only — no `any`.

### Automation & Integration Agent — `.github/workflows/`, `.lighthouserc.cjs`
CI pipeline, uv environment caching, parallelized GitHub Actions jobs.
Any build failure must break the pipeline before merge.

### QA Agent — `frontend/playwright.config.ts`, `frontend/vitest.config.ts`, `tests/` · `/qa <task>`
Unit, component, and e2e tests. Axe-core injection in Playwright workflows.
Assert Lighthouse accessibility score ≥ 95. Structural HTML invalidity must fail the suite.

### Archivist Agent — `README.md`, `TODO.md`, `ARCHITECTURE.md`, docstrings · `/docs-sync <task>`
Keep `TODO.md` synchronized with sprint state after every merge.
Strip boilerplate from all output. Dense, actionable prose only.

### Multi-Agent Orchestration — `backend/agents/`

```
coordinator.py       — delegates to Route + Crew agents, validates output against FlightState
route_analytics.py   — reads telemetry anomalies, queries weather/runway mock data
crew_logistics.py    — computes crew duty time limits and gate constraints
```

---

## Knowledge Base

`.knowledge_base/` is the authoritative reference for every framework in the stack.
Use it before writing implementation code for a new area.

### How to use it
- **Start at** `.knowledge_base/MAP.md` — it maps every topic to a leaf file.
- **Read the relevant leaf** for Key Patterns and Gotchas before writing code in that domain.
- **Add links to** `## Resources` in the matching leaf when the user provides reference URLs.
  The Archivist Agent synthesizes those links into the Key Patterns and Gotchas sections.
- **Update leaves** when you discover a real-world gotcha the file doesn't cover.

### Archivist responsibilities
When the user drops a link, run `/kb-update <url>`. The skill handles fetch → leaf
identification → synthesis → resource entry automatically.

---

## Skills

Project-level slash commands in `.claude/commands/`. Invoke from any Claude Code session.

| Skill | Purpose |
|---|---|
| `/validate` | Runs the full check suite — ruff, mypy, pytest, tsc, vitest — and reports pass/fail |
| `/contract-check` | Diffs `FlightState` (Pydantic) against TypeScript interfaces; flags any drift |
| `/sync-todo` | Rewrites `TODO.md` from `git log` + codebase state |
| `/kb-update <url>` | Fetches a URL and synthesizes it into the matching knowledge base leaf |
| `/backend <task>` | Activates Backend Core Agent; reads KB leaves before writing code |
| `/frontend <task>` | Activates Frontend UX Agent; reads KB leaves before writing code |
| `/qa <task>` | Activates QA Agent; reads KB leaves before writing tests |
| `/docs-sync <task>` | Activates Archivist Agent for documentation and KB maintenance |

---

## Branch & PR Protocol

- Prefixes: `feat/`, `fix/`, `docs/`, `ci/`
- **Never commit directly to `main`**
- Sync before branching: `git checkout main && git pull origin main`
- Every PR requires: one human approval (the other partner) + all CI checks green
- Merge strategy: **Squash and Merge only** (preserves linear history for semantic-release)

### PR Description Template

1. **Context:** Which PRD item or problem does this address?
2. **Impact:** What changed across the frontend/backend boundary?
3. **Verification:** Paste local test output (`pytest`, `vitest`, `playwright`).

---

## Commit Convention

Format: `type(scope): description`

Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

Use `cz commit` for an interactive prompt. Commitlint validates every commit via Husky.

---

## Code Standards

- **Python:** PEP-8, explicit type hints everywhere, Google-style docstrings
- **TypeScript:** `strict: true`, immutable interfaces from the data contract
- **Comments:** Only for non-obvious WHY — never narrate what the code does
- **Empty states:** Always render intentional fallback copy, never raw `0` or blank strings
- **No AI smell:** No boilerplate comments, no self-evident prose, no "it's not just X, it's Y"
