import { expect, test } from "@playwright/test";

test("supports cited answer, reviewable draft, and task creation", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "教学管理副职工作台" }),
  ).toBeVisible();

  await page.getByRole("button", { name: /带来源回答/ }).click();
  await expect(page.getByText("来源支持以下要点")).toBeVisible();

  await page.getByRole("button", { name: /生成草稿/ }).click();
  await expect(
    page.getByText("待人工审核，不得直接作为正式通知或决定"),
  ).toBeVisible();

  await page.getByRole("button", { name: /加入任务台账/ }).click();
  await expect(page.getByText(/审核草稿/).first()).toBeVisible();
});
