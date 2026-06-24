import { expect, test } from "@playwright/test";

test.describe("Public portfolio", () => {
  test("home page loads with main portfolio content", async ({
    page,
  }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/Bajirao/i);

    await expect(
      page.getByText(/Bajirao/i).first(),
    ).toBeVisible();

    await expect(
      page.getByText(/AI/i).first(),
    ).toBeVisible();
  });

  test("AI tools route loads directly", async ({
    page,
  }) => {
    await page.goto("/ai-tools");

    await expect(page).toHaveURL(/\/ai-tools/);

    await expect(
      page.getByText(/job/i).first(),
    ).toBeVisible();
  });

  test("admin login route loads directly", async ({
    page,
  }) => {
    await page.goto("/admin/login");

    await expect(page).toHaveURL(/\/admin\/login/);

    await expect(
      page.getByRole("heading", {
        name: /admin login/i,
      }),
    ).toBeVisible();
  });

  test("project detail route does not show Vercel 404", async ({
    page,
  }) => {
    await page.goto("/projects/recruitai-pro");

    await expect(page).not.toHaveTitle(/404/i);

    await expect(
      page.locator("body"),
    ).not.toContainText("404: NOT_FOUND");
  });

  test("research detail route does not show Vercel 404", async ({
    page,
  }) => {
    await page.goto("/research/hindi-event-extraction");

    await expect(page).not.toHaveTitle(/404/i);

    await expect(
      page.locator("body"),
    ).not.toContainText("404: NOT_FOUND");
  });
});