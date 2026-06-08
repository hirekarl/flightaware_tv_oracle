# GitHub Actions

**Role:** CI pipeline. Four parallelized jobs gate every push and PR to `main`/`develop`.
The `automated-release` job runs only on merge to `main` after all three validation jobs pass.

---

## Pipeline Overview

```
push / PR to main or develop
├── backend-validation      (ruff, mypy, pytest)
├── frontend-validation     (lint, tsc, vitest, playwright)
└── accessibility-audit     (LHCI ≥ 95)  ← needs frontend-validation

merge to main only
└── automated-release       (semantic-release) ← needs all three above
```

## Key Patterns

### Job structure skeleton
```yaml
jobs:
  backend-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - name: Cache uv store
        uses: actions/cache@v4
        with:
          path: ~/.cache/uv
          key: ${{ runner.os }}-uv-${{ hashFiles('pyproject.toml') }}
      - run: uv sync --group dev
      - run: uv run ruff check backend/ tests/
      - run: uv run mypy backend/ --strict
      - run: uv run pytest
```

### Conditional job (merge to main only)
```yaml
automated-release:
  needs: [backend-validation, frontend-validation, accessibility-audit]
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  permissions:
    contents: write
```

### Required secrets
| Secret | Used by |
|---|---|
| `GH_TOKEN` | `automated-release` — semantic-release needs write access |
| `GEMINI_API_KEY` | Add if integration tests call the real API (currently mocked) |

---

## Gotchas

- `actions/cache` on `pyproject.toml` hash is correct. If `uv.lock` is committed
  (it should be), cache on `uv.lock` instead for tighter invalidation.
- `astral-sh/setup-uv@v4` automatically installs the latest stable uv. Pin to a
  specific version tag if you need reproducibility across re-runs.
- `permissions: contents: write` on the release job is required for semantic-release
  to push version commits and create tags. Scope it to that job only.
- Playwright in CI installs with `--with-deps chromium` to pull in system deps.
  This is already in the `frontend-validation` job.
- The `accessibility-audit` job re-builds the frontend. Cache `frontend/node_modules`
  with `actions/setup-node cache: "npm"` to avoid a full `npm ci` on every run.

---

## Resources

<!-- Drop links here — Archivist will synthesize -->
