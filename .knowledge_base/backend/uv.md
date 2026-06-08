# uv

**Version:** latest (pinned via `astral-sh/setup-uv@v4` in CI)
**Role:** Replaces pip + venv + pip-tools. All Python commands in this project run
through `uv run`. Manages both production deps and the `dev` dependency group.

---

## Key Patterns

### Daily commands
```bash
uv sync --group dev          # install all deps including dev group
uv run uvicorn backend.main:app --reload   # run the API
uv run pytest                # run tests
uv run ruff check backend/   # lint
uv run mypy backend/ --strict
uv run cz commit             # interactive conventional commit
```

### Adding dependencies
```bash
uv add fastapi               # add to [project.dependencies]
uv add --group dev pytest    # add to [dependency-groups].dev
uv remove langchain-core     # remove
```

### pyproject.toml dep format
```toml
[project]
dependencies = [
    "fastapi[standard]>=0.115.0",
]

[dependency-groups]
dev = [
    "pytest>=8.3.0",
]
```
`[dependency-groups]` is uv's native format (PEP 735). Prefer it over
`[project.optional-dependencies]` for dev tooling.

### Lock file
`uv.lock` is auto-generated. Commit it for reproducible CI installs.
Re-lock after any dep change: `uv lock`.

---

## Gotchas

- `uv run <cmd>` always activates the project's virtual env. Don't manually activate
  `.venv` — just prefix every command with `uv run`.
- `uv sync` without `--group dev` installs production deps only. CI jobs that need
  ruff/mypy/pytest must use `--group dev`.
- The uv cache lives at `~/.cache/uv`. In CI, cache on `pyproject.toml` hash to
  avoid stale installs while keeping fast restores.
- `uv pip install` bypasses the project's `pyproject.toml` — avoid it. Use `uv add`
  to keep the lockfile in sync.

---

## Resources

<!-- Drop links here — Archivist will synthesize -->
