#!/usr/bin/env bash
# PostToolUse auto-formatter. Reads the hook JSON from stdin, extracts the
# written file path, and dispatches to the appropriate formatter.
#
# Backend .py in backend/ or tests/  →  ruff check --fix + ruff format
# Frontend .ts/.tsx in frontend/     →  prettier --write

input=$(cat)
[[ -z "$input" ]] && exit 0

script_dir=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
file_path=$(printf '%s' "$input" | python3 "$script_dir/extract_path.py" 2>/dev/null) || true

[[ -z "$file_path" ]] && exit 0

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
repo_root="${repo_root//\\//}"

# ── Backend: Python files in backend/ or tests/ ───────────────────────────────
if [[ "$file_path" =~ \.py$ ]] && [[ "$file_path" =~ /(backend|tests)/ ]]; then
  cd "$repo_root"
  uv run ruff check --fix "$file_path" 2>&1 || true
  uv run ruff format "$file_path" 2>&1 || true
  remaining=$(uv run ruff check "$file_path" 2>&1)
  [[ $? -ne 0 ]] && printf '[ruff] Manual fix needed:\n%s\n' "$remaining"
  true
fi

# ── Frontend: TypeScript/TSX files in frontend/ ───────────────────────────────
if [[ "$file_path" =~ \.(ts|tsx)$ ]] && [[ "$file_path" =~ /frontend/ ]]; then
  cd "$repo_root/frontend"
  rel="${file_path#*/frontend/}"
  npx prettier --write "$rel" 2>&1 || true
fi
