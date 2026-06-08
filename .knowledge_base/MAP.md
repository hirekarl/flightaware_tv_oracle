# Knowledge Base — FlightAware TV

Leaf files contain usage patterns, gotchas, and synthesized notes for each framework.
Drop reference links into the `## Resources` section of the relevant leaf; the Archivist
Agent will synthesize them into the **Key Patterns** and **Gotchas** sections.

---

## Backend

| Topic | File | Role in stack |
|---|---|---|
| FastAPI + Uvicorn | [backend/fastapi.md](backend/fastapi.md) | HTTP framework, SSE endpoint, lifespan |
| Pydantic v2 | [backend/pydantic-v2.md](backend/pydantic-v2.md) | Data contract enforcement, validation |
| Instructor + google-genai | [backend/instructor-gemini.md](backend/instructor-gemini.md) | Structured LLM output via Gemini |
| uv | [backend/uv.md](backend/uv.md) | Dependency management, virtual envs, CI |
| Ruff + mypy | [backend/ruff-mypy.md](backend/ruff-mypy.md) | Lint, format, strict type checking |

## Frontend

| Topic | File | Role in stack |
|---|---|---|
| React 19 | [frontend/react-19.md](frontend/react-19.md) | UI framework, SSE client hook |
| Vite + Vitest | [frontend/vite-vitest.md](frontend/vite-vitest.md) | Build tool, unit/component testing |
| Playwright + axe-core | [frontend/playwright-axe.md](frontend/playwright-axe.md) | E2e testing, a11y audit injection |
| TypeScript (strict) | [frontend/typescript.md](frontend/typescript.md) | Type safety, data contract interfaces |

## Infrastructure

| Topic | File | Role in stack |
|---|---|---|
| GitHub Actions | [infra/github-actions.md](infra/github-actions.md) | CI pipeline (4 parallelized jobs) |
| Lighthouse CI | [infra/lhci.md](infra/lhci.md) | Automated a11y score gate (≥ 95) |
| semantic-release + commitizen | [infra/semantic-release-commitizen.md](infra/semantic-release-commitizen.md) | Versioning, changelog, cz commit UX |
| Husky + commitlint | [infra/husky-commitlint.md](infra/husky-commitlint.md) | Commit message enforcement |
