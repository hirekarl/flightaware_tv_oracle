# Lighthouse CI (LHCI)

**Package:** `@lhci/cli` (v0.15.1 as of 2026-06-08; install globally in CI)
**Role:** Automated accessibility score gate. Asserts `categories:accessibility ≥ 0.95`
on the production Vite build. Blocks merge if the score drops below threshold.

---

## Key Patterns

### .lighthouserc.js structure
```javascript
module.exports = {
  ci: {
    collect: {
      staticDistDir: './frontend/dist',   // relative to where lhci autorun is called
      numberOfRuns: 3,                    // average over 3 runs to reduce variance
    },
    assert: {
      preset: 'lighthouse:no-pwa',        // skip PWA checks
      assertions: {
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['warn', { minScore: 0.9 }],
        'categories:performance': ['warn', { minScore: 0.8 }],
      },
    },
    upload: {
      target: 'temporary-public-storage', // posts results to lhci.dev for PR status links
    },
  },
};
```

### Running locally
```bash
cd frontend && npm run build     # must build first
cd ..                            # run lhci from repo root (where .lighthouserc.js lives)
lhci autorun
```

### CI step
```yaml
- name: Install LHCI
  run: npm install -g @lhci/cli@0.15.x
- name: Run Lighthouse CI
  run: lhci autorun
  env:
    LHCI_GITHUB_APP_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Assertion levels
- `'error'` — fails the CI job if the score is below `minScore`
- `'warn'` — logs a warning but does not fail the job

---

## Gotchas

- `lhci autorun` must be called from the directory containing `.lighthouserc.js`
  (repo root in this project). The `staticDistDir` path is relative to that location.
- `numberOfRuns: 3` reduces accessibility score variance from a cold single run.
  Accessibility scores are generally stable; performance fluctuates more.
- `temporary-public-storage` upload is unauthenticated and public. Don't use it for
  apps with sensitive UI. Disable uploads by removing the `upload` block if needed.
- `lighthouse:no-pwa` preset is required — without it, the PWA category failure
  blocks the assertion even though this project doesn't target PWA.
- LHCI GitHub status checks appear in PRs when `LHCI_GITHUB_APP_TOKEN` is set.
  Use `secrets.GITHUB_TOKEN` (auto-provided) rather than a personal token.
- The `frontend/dist/` build must exist before `lhci autorun`. The accessibility
  job re-runs `npm ci && npm run build` to ensure a fresh artifact.

---

## Resources

- https://github.com/GoogleChrome/lighthouse-ci/ (LHCI GitHub — fetched 2026-06-08, v0.15.1)
<!-- Drop additional links here — Archivist will synthesize -->
