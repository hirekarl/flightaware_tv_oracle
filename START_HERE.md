# Start Here — Ahsan

You own the frontend: `frontend/src/`. React 19, TypeScript, Vitest, Playwright.
Karl owns the backend. You consume his SSE stream via a typed data contract — you never touch `backend/`.

---

## 1. Get your environment running

Follow [`docs/contributor-setup.md`](docs/contributor-setup.md) in order.
It covers Python (you don't need to install it separately — `uv` handles it), Node,
GitHub CLI SSL fix, and browser-based authentication.

---

## 2. Read these (in this order)

| Doc | What you're looking for |
|---|---|
| [`README.md`](README.md) | Repo layout, API endpoints, CI pipeline overview |
| [`frontend/src/types/flight.ts`](frontend/src/types/flight.ts) | The data contract — every component you build consumes these types |
| [`CLAUDE.md` → Workflows → Ahsan's loop](CLAUDE.md) | Your day-to-day skill invocation pattern |
| [`.knowledge_base/frontend/`](.knowledge_base/frontend/) | React 19, TypeScript, Vitest, and Playwright gotchas for this stack |

---

## 3. Your daily commands

```bash
# Start the frontend dev server (open a second terminal for the backend if needed)
cd frontend && npm run dev
# → http://localhost:5173

# Run unit tests
cd frontend && npm run test:unit

# Run e2e tests (requires dev server running)
cd frontend && npm run test:e2e

# Full check suite before pushing
/validate
```

---

## 4. Your workflow for a new feature


/orchestrate <feature description>   ← writes failing tests, confirms red
/frontend <task>                     ← implements to pass the tests
/qa <task>                           ← adds Playwright e2e coverage
/validate                            ← must be clean before you push
```

Then: `git push origin feat/frontend-<feature>` → open PR → Karl reviews → CI green → Squash and Merge.

---

## 5. When to talk to Karl

- The feature requires a change to the data contract (`FlightState` fields or structure)
- You need a new endpoint or a change to an existing one
- `/contract-check` reports drift between the Pydantic models and your TypeScript interfaces

For contract changes: agree on the schema together first, then run `/contract-check` to confirm
both sides are aligned before writing any feature code.
