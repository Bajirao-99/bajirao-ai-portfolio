import { expect, test } from "@playwright/test";

test.describe("Admin authentication", () => {
  test("admin login page loads", async ({
    page,
  }) => {
    await page.goto("/admin/login");

    await expect(
      page.getByRole("heading", {
        name: /admin login/i,
      }),
    ).toBeVisible();

    await expect(
      page.locator('input[autocomplete="username"]'),
    ).toBeVisible();

    await expect(
      page.locator('input[type="password"]'),
    ).toBeVisible();
  });

  test("protected admin dashboard redirects to login", async ({
    page,
  }) => {
    await page.goto("/admin");

    await expect(page).toHaveURL(/\/admin\/login/);
  });
});