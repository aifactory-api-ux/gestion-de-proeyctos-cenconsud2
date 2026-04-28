# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: buttons.spec.ts >> Botones de ProjectDetails >> botón Request Forecast existe y es clickeable
- Location: tests-functional/buttons.spec.ts:20:3

# Error details

```
Error: Channel closed
```

```
Error: expect(locator).toBeVisible() failed

Locator: getByRole('button', { name: /request forecast/i })
Expected: visible
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByRole('button', { name: /request forecast/i })

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - heading "Cenconsud2 Project Management" [level=1] [ref=e5]
    - generic [ref=e6]:
      - generic [ref=e7]:
        - strong [ref=e8]: Admin User
        - text: admin
        - text: admin@cenconsud2.com
      - button "Logout" [ref=e9] [cursor=pointer]
  - generic [ref=e11]:
    - heading "Projects" [level=2] [ref=e12]
    - paragraph [ref=e13]: Network Error
    - paragraph [ref=e14]: No projects available.
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Botones de UserMenu', () => {
  4  |   test('botón Logout existe y es clickeable', async ({ page }) => {
  5  |     await page.goto('/');
  6  |     const logoutBtn = page.getByRole('button', { name: /logout/i });
  7  |     await expect(logoutBtn).toBeVisible();
  8  |     await expect(logoutBtn).toBeEnabled();
  9  |   });
  10 | 
  11 |   test('botón Logout llama al handler', async ({ page }) => {
  12 |     await page.goto('/');
  13 |     await page.getByRole('button', { name: /logout/i }).click();
  14 |     const consoleMessages: string[] = [];
  15 |     page.on('console', msg => consoleMessages.push(msg.text()));
  16 |   });
  17 | });
  18 | 
  19 | test.describe('Botones de ProjectDetails', () => {
  20 |   test('botón Request Forecast existe y es clickeable', async ({ page }) => {
  21 |     await page.goto('/');
  22 |     const forecastBtn = page.getByRole('button', { name: /request forecast/i });
> 23 |     await expect(forecastBtn).toBeVisible();
     |                               ^ Error: expect(locator).toBeVisible() failed
  24 |     await expect(forecastBtn).toBeEnabled();
  25 |   });
  26 | 
  27 |   test('botón Request Forecast llama al handler', async ({ page }) => {
  28 |     await page.goto('/');
  29 |     const consoleMessages: string[] = [];
  30 |     page.on('console', msg => consoleMessages.push(msg.text()));
  31 |   });
  32 | });
  33 | 
  34 | test.describe('Botones de ProjectList', () => {
  35 |   test('elementos de lista son clickeables', async ({ page }) => {
  36 |     await page.goto('/');
  37 |   });
  38 | });
```