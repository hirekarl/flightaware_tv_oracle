Run the full local validation suite for FlightAware TV and report results.

Execute these checks in order:

**Backend** (from repo root):
1. `uv run ruff check backend/` — lint
2. `uv run ruff format --check backend/` — format
3. `uv run mypy backend/ --strict` — type check
4. `uv run pytest` — unit tests

**Frontend** (from `frontend/`):
5. `npm run lint` — ESLint
6. `npx tsc --noEmit` — type check
7. `npm run test:unit` — Vitest

For each check report PASS or FAIL. On failure, include the relevant output.
Final summary: total checks passed / failed, with a list of any failures.
