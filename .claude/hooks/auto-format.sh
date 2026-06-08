#!/usr/bin/env bash
# PostToolUse auto-formatter. Reads the hook JSON from stdin, extracts the
# written file path, and dispatches to the appropriate formatter.
#
# Backend .py in backend/ or tests/  →  ruff check --fix + ruff format
# Frontend .ts/.tsx in frontend/     →  prettier --write

input=$(cat)

file_path=$(echo "$input" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    fp = d.get('tool_input', {}).get('file_path', '')
    print(fp.replace('\\\\', '/'))
except Exception:
    pass
" 2>/dev/null) || true

[[ -z "$file_path" ]] && exit 0

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
repo_root="${repo_root//\\//}"

# ── Backend: Python files in backend/ or tests/ ───────────────────────────────
if [[ "$file_path" =~ \.py$ ]] && [[ "$file_path" =~ /(backend|tests)/ ]]; then
  cd "$repo_root"
  uv run ruff check --fix "$file_path" 2>&1 || true
  uv run ruff format "$file_path" 2>&1 || true
  remaining=$(uv run ruff check "$file_path" 2>&1) || true
  [[ -n "$remaining" ]] && printf '[ruff] Manual fix needed:\n%s\n' "$remaining"
fi

# ── Frontend: TypeScript/TSX files in frontend/ ───────────────────────────────
if [[ "$file_path" =~ \.(ts|tsx)$ ]] && [[ "$file_path" =~ /frontend/ ]]; then
  cd "$repo_root/frontend"
  rel="${file_path#*/frontend/}"
  npx --no prettier --write "$rel" 2>&1 || true
fi
