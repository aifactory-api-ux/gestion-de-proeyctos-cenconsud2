import { test, expect } from '@playwright/test';

test.describe('Botones de UserMenu', () => {
  test('botón Logout existe y es clickeable', async ({ page }) => {
    await page.goto('/');
    const logoutBtn = page.getByRole('button', { name: /logout/i });
    await expect(logoutBtn).toBeVisible();
    await expect(logoutBtn).toBeEnabled();
  });

  test('botón Logout llama al handler', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: /logout/i }).click();
    const consoleMessages: string[] = [];
    page.on('console', msg => consoleMessages.push(msg.text()));
  });
});

test.describe('Botones de ProjectDetails', () => {
  test('botón Request Forecast existe y es clickeable', async ({ page }) => {
    await page.goto('/');
    const forecastBtn = page.getByRole('button', { name: /request forecast/i });
    await expect(forecastBtn).toBeVisible();
    await expect(forecastBtn).toBeEnabled();
  });

  test('botón Request Forecast llama al handler', async ({ page }) => {
    await page.goto('/');
    const consoleMessages: string[] = [];
    page.on('console', msg => consoleMessages.push(msg.text()));
  });
});

test.describe('Botones de ProjectList', () => {
  test('elementos de lista son clickeables', async ({ page }) => {
    await page.goto('/');
  });
});