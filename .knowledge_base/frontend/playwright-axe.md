# Playwright + @axe-core/playwright

**Versions:** `@playwright/test>=1.49`, `@axe-core/playwright>=4.10`
**Role:** End-to-end browser testing with automated accessibility auditing injected
into every test workflow. Replaces manual Lighthouse runs during development.

---

## Key Patterns

### Basic e2e test structure
```typescript
import { test, expect } from '@playwright/test';

test('CRITICAL flight sorts to top of queue', async ({ page }) => {
  await page.goto('/');
  const cards = page.getByRole('article');
  await expect(cards.first()).toHaveAttribute('data-status', 'CRITICAL');
});
```
Use `getByRole`, `getByLabel`, `getByTestId` — these locators are resilient to DOM
restructuring and align with how assistive technologies navigate the page.

### Full-page axe-core audit
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('fleet queue has no accessibility violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

### Scoping an audit to a specific component
```typescript
const results = await new AxeBuilder({ page })
  .include('#flight-queue')          // only audit this subtree
  .withTags(['wcag2a', 'wcag2aa'])   // WCAG 2.0 A + AA rules only
  .analyze();
```

### Handling a known violation temporarily
```typescript
// Disable a specific rule rather than excluding whole elements (less coarse).
const results = await new AxeBuilder({ page })
  .disableRules(['color-contrast'])  // remove once design tokens are finalized
  .analyze();
```
Avoid `exclude()` for this — it suppresses ALL rules for the element, not just
the known one.

### Waiting for dynamic content before auditing
```typescript
await page.waitForSelector('[data-status="CRITICAL"]'); // wait for SSE data to arrive
const results = await new AxeBuilder({ page }).analyze();
```
Always call `analyze()` after the page reaches the desired state, not immediately
after `goto()`.

### Attaching full results to the report (debugging)
```typescript
test('audit with full report', async ({ page }, testInfo) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  await testInfo.attach('accessibility-scan-results', {
    body: JSON.stringify(results, null, 2),
    contentType: 'application/json',
  });
  expect(results.violations).toEqual([]);
});
```

### playwright.config.ts essentials
```typescript
webServer: {
  command: 'npm run dev',
  url: 'http://localhost:5173',
  reuseExistingServer: !process.env.CI,  // reuse local dev server, fresh in CI
},
```

---

## Gotchas

- Automated axe-core catches ~30–40% of WCAG issues. Manual testing is required
  for the remainder — particularly keyboard nav and screen reader flow.
- `exclude()` is overly broad: it suppresses all axe rules for the element and all
  its descendants. Prefer `disableRules(['specific-rule'])`.
- Don't snapshot the full `violations` array — it contains rendered HTML snippets
  that break on any DOM change. Assert `violations.toEqual([])` or snapshot only
  `violations.map(v => ({ id: v.id, targets: v.nodes.map(n => n.target) }))`.
- `forbidOnly: !!process.env.CI` blocks `.only` tests from merging. Remove before push.
- Playwright runs with `workers: 1` in CI to avoid port conflicts. Locally it
  parallelizes automatically.
- Install browsers before first run: `npx playwright install --with-deps chromium`.
  The CI `frontend-validation` job handles this.

---

## Resources

- https://playwright.dev/docs/accessibility-testing (axe-core integration docs — fetched 2026-06-08)
- https://playwright.dev/ (Playwright homepage — fetched 2026-06-08)
<!-- Drop additional links here — Archivist will synthesize -->
