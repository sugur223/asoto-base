import { test, expect } from '@playwright/test';

test.describe('サンプルテスト', () => {
  test('基本的なナビゲーション', async ({ page }) => {
    // ログインページに移動
    await page.goto('/login');

    // ページタイトルを確認
    await expect(page).toHaveTitle(/asotobase/i);

    // ページの基本要素を確認
    const body = await page.locator('body');
    await expect(body).toBeVisible();
  });
});
