/**
 * Phase 2 Full-Stack Todo App - Accessibility Tests (T076)
 *
 * Uses axe-core to audit pages for WCAG 2.1 Level AA compliance.
 * Run with: npm run test:a11y
 */

import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

// Configure axe to check for WCAG 2.1 Level AA
const axeConfig = {
  // Check against WCAG 2.1 Level AA
  runOnly: {
    type: "tag" as const,
    values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"],
  },
};

test.describe("Accessibility Audit - Public Pages", () => {
  test("signin page should have no critical accessibility violations", async ({
    page,
  }) => {
    await page.goto("/signin");

    // Wait for page to be fully loaded
    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    // Filter for critical and serious violations only
    const criticalViolations = accessibilityScanResults.violations.filter(
      (v) => v.impact === "critical" || v.impact === "serious"
    );

    // Log violations for debugging
    if (criticalViolations.length > 0) {
      console.log("Critical/Serious violations on /signin:");
      criticalViolations.forEach((v) => {
        console.log(`  - ${v.id}: ${v.description}`);
        console.log(`    Impact: ${v.impact}`);
        console.log(`    Help: ${v.helpUrl}`);
      });
    }

    expect(criticalViolations).toHaveLength(0);
  });

  test("signup page should have no critical accessibility violations", async ({
    page,
  }) => {
    await page.goto("/signup");

    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    const criticalViolations = accessibilityScanResults.violations.filter(
      (v) => v.impact === "critical" || v.impact === "serious"
    );

    if (criticalViolations.length > 0) {
      console.log("Critical/Serious violations on /signup:");
      criticalViolations.forEach((v) => {
        console.log(`  - ${v.id}: ${v.description}`);
        console.log(`    Impact: ${v.impact}`);
      });
    }

    expect(criticalViolations).toHaveLength(0);
  });
});

test.describe("Accessibility Audit - Form Interactions", () => {
  test("signin form should have proper labels and focus management", async ({
    page,
  }) => {
    await page.goto("/signin");
    await page.waitForLoadState("networkidle");

    // Check that all form inputs have associated labels
    const emailInput = page.getByLabel(/email/i);
    const passwordInput = page.getByLabel(/password/i);

    await expect(emailInput).toBeVisible();
    await expect(passwordInput).toBeVisible();

    // Check keyboard navigation
    await emailInput.focus();
    expect(await page.evaluate(() => document.activeElement?.tagName)).toBe(
      "INPUT"
    );

    // Tab to password field
    await page.keyboard.press("Tab");
    expect(
      await page.evaluate(
        () => (document.activeElement as HTMLInputElement)?.type
      )
    ).toBe("password");
  });

  test("signup form should have proper labels and focus management", async ({
    page,
  }) => {
    await page.goto("/signup");
    await page.waitForLoadState("networkidle");

    // Check that all form inputs have associated labels
    const nameInput = page.getByLabel(/name/i);
    const emailInput = page.getByLabel(/email/i);
    const passwordInput = page.getByLabel(/password/i);

    await expect(nameInput).toBeVisible();
    await expect(emailInput).toBeVisible();
    await expect(passwordInput).toBeVisible();
  });
});

test.describe("Accessibility Audit - Color Contrast", () => {
  test("signin page should have sufficient color contrast", async ({
    page,
  }) => {
    await page.goto("/signin");
    await page.waitForLoadState("networkidle");

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2aa"])
      .options({ rules: { "color-contrast": { enabled: true } } })
      .analyze();

    const contrastViolations = results.violations.filter(
      (v) => v.id === "color-contrast"
    );

    if (contrastViolations.length > 0) {
      console.log("Color contrast violations:");
      contrastViolations.forEach((v) => {
        v.nodes.forEach((node) => {
          console.log(`  - Element: ${node.target}`);
          console.log(`    HTML: ${node.html.substring(0, 100)}`);
        });
      });
    }

    expect(contrastViolations).toHaveLength(0);
  });
});

test.describe("Accessibility Audit - Keyboard Navigation", () => {
  test("all interactive elements should be keyboard accessible", async ({
    page,
  }) => {
    await page.goto("/signin");
    await page.waitForLoadState("networkidle");

    // Get all focusable elements
    const focusableElements = await page.evaluate(() => {
      const selector =
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
      const elements = document.querySelectorAll(selector);
      return elements.length;
    });

    // Should have at least email, password, and submit button
    expect(focusableElements).toBeGreaterThanOrEqual(3);

    // Test tab navigation through all elements
    let tabCount = 0;
    const maxTabs = 10;

    while (tabCount < maxTabs) {
      await page.keyboard.press("Tab");
      const activeElement = await page.evaluate(() => {
        const el = document.activeElement;
        return {
          tag: el?.tagName,
          type: (el as HTMLInputElement)?.type,
          visible: el?.checkVisibility?.() ?? true,
        };
      });

      // All focused elements should be visible
      expect(activeElement.visible).toBe(true);
      tabCount++;
    }
  });
});
