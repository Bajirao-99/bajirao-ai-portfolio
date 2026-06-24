import { expect, test } from "@playwright/test";

test.describe("AI tools page", () => {
  test("job matcher form is visible", async ({
    page,
  }) => {
    await page.goto("/ai-tools");

    await expect(
      page.getByText(/job description/i).first(),
    ).toBeVisible();

    await expect(
      page.locator("textarea").first(),
    ).toBeVisible();
  });

  test("portfolio chatbot launcher is visible", async ({
    page,
  }) => {
    await page.goto("/");

    const possibleChatButtons =
      page.getByRole("button", {
        name: /portfolio assistant|chat|ai/i,
      });

    await expect(
      possibleChatButtons.first(),
    ).toBeVisible();
  });
});