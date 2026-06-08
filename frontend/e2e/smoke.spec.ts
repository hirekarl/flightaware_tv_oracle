import { test, expect } from '@playwright/test';

test('app shell renders', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle('FlightAware TV — Fleet Disruption Oracle');
  await expect(page.getByRole('heading', { name: 'FlightAware TV' })).toBeVisible();
});
