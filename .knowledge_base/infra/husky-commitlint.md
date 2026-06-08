# Husky + commitlint

**Versions:** `husky>=9.0`, `@commitlint/cli>=19`, `@commitlint/config-conventional>=19`
**Role:** Local git hook enforcement. The `commit-msg` hook runs on every `git commit`,
strips Claude/Anthropic co-authorship lines, then validates the message format against
the Conventional Commits spec.

---

## Key Patterns

### Setup (first time on a cloned repo)
```bash
npm install          # installs husky from root package.json
# husky auto-installs hooks via the `prepare` script
```

### .husky/commit-msg hook
```sh
#!/usr/bin/env sh
# Strip Claude/Anthropic co-authored-by lines, then validate.
if [ -f "$1" ]; then
  node -e "
const fs = require('fs');
const msg = fs.readFileSync(process.argv[1], 'utf8');
const cleaned = msg.split('\n')
  .filter(l => !/^Co-authored-by:.*(?:claude|anthropic)/i.test(l))
  .join('\n');
fs.writeFileSync(process.argv[1], cleaned);
" "$1"
fi
npx --no -- commitlint --edit "$1"
```

### commitlint.config.js
```javascript
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert',
    ]],
  },
};
```

### Valid commit format
```
feat(backend): add SSE fleet stream endpoint
fix(frontend): resolve critical card z-index flicker
docs(kb): synthesize Pydantic v2 notes into knowledge base
```

---

## Gotchas

- Husky v9 hooks live in `.husky/` at the root where `package.json` is. The hook
  file must exist — Husky does not create it automatically.
- On Windows, `.husky/commit-msg` runs via Git Bash (sh). The Node.js one-liner in
  the hook works cross-platform because Node is invoked explicitly.
- `npx --no --` prevents npx from installing commitlint if it's missing. CI should
  have it via `npm ci`; local should have it via `npm install`.
- commitlint validates the message *after* the co-authorship strip. If a commit
  message is otherwise malformed (wrong type, missing description), commitlint will
  reject it.
- The root `package.json` is separate from `frontend/package.json`. Running
  `npm install` in the repo root installs Husky; running it in `frontend/` installs
  the frontend deps. Both are needed.
- Husky hooks do **not** run on `--no-verify` commits. That flag should never be
  used except in emergencies — and even then the co-authorship concern remains.

---

## Resources

<!-- Drop links here — Archivist will synthesize -->
