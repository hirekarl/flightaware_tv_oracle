# Ruff + mypy

**Versions:** `ruff>=0.8`, `mypy>=2.0` (current: mypy 2.1, released May 2026)
**Role:** Ruff handles all linting, formatting, and import sorting (replaces black +
isort + flake8). mypy runs in strict mode to catch type errors before CI.

---

## Key Patterns

### Running locally
```bash
uv run ruff check backend/ tests/          # lint
uv run ruff check --fix backend/ tests/   # lint + auto-fix
uv run ruff format backend/ tests/        # format (replaces black)
uv run mypy backend/ --strict              # type check
```

### pyproject.toml config
```toml
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
# E = pycodestyle errors, F = pyflakes, W = pycodestyle warnings
# I = isort (import sorting) — replaces isort package entirely

[tool.ruff.lint.isort]
known-first-party = ["backend"]

[tool.mypy]
python_version = "3.12"
strict = true
disallow_untyped_defs = true
warn_unused_ignores = true
no_implicit_optional = true
```

### Ruff replaces (do not install these separately)
- `black` → `ruff format`
- `isort` → `ruff check` with `I` rules
- `flake8` (and many plugins) → `ruff check` with `E`, `F`, `W` rules
- `pydocstyle` → add `D` to `select`

### Common mypy strict errors to know
```
error: Function is missing a return type annotation
→ Add -> ReturnType; use -> None for procedures including __init__

error: Call to untyped function in typed context
→ Library has no stubs. Add types-<pkg> stub package or # type: ignore[no-untyped-call]

error: Incompatible default for argument "x" (default has type "None", argument has type "T")
→ Change param to T | None or Optional[T]

error: Module "x" has no attribute "y"
→ Missing __init__.py export or stubs. Add __all__ to the module.
```

### Pydantic + mypy
Pydantic v2 ships its own mypy plugin. Add to `pyproject.toml`:
```toml
[tool.mypy]
plugins = ["pydantic.mypy"]
```
Without this, mypy may not recognize `BaseModel` field validation.

---

## Gotchas

- Ruff's `I` ruleset handles import sorting — do **not** install `isort` alongside it.
- `ruff format` and `black` are not identical. Ruff format is canonical for this
  project — do not run black.
- CI runs `ruff format --check` (read-only); local `ruff format` applies the fix.
- `warn_unused_ignores = true` turns stale `# type: ignore` comments into errors.
  Remove them when upstream adds types.
- mypy strict requires annotations on all functions, including test helpers.
- mypy v2.x+ has improved inference — some `# type: ignore` comments that were
  needed in v1.x may now be stale and will error under `warn_unused_ignores`.

---

## Resources

- https://docs.astral.sh/ruff/ (Ruff docs — fetched 2026-06-08)
- https://mypy-lang.org/ (mypy homepage, v2.1 — fetched 2026-06-08)
