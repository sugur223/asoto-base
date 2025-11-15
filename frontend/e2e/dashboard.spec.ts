import { test, expect } from '@playwright/test';

// テストユーザーでログインするヘルパー関数
async function login(page: any) {
  await page.goto('/login');
  await page.getByLabel(/メールアドレス/i).fill('test@example.com');
  await page.getByLabel(/パスワード/i).fill('password123');
  await page.getByRole('button', { name: /ログイン/i }).click();
  await page.waitForURL('/dashboard', { timeout: 5000 });
}

test.describe('ダッシュボード', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('ダッシュボードが表示される', async ({ page }) => {
    // ダッシュボードのheading確認
    await expect(page.getByRole('heading', { name: /ダッシュボード/i })).toBeVisible();

    // 4つの統計カードを確認（first()使用で重複回避）
    await expect(page.getByText(/累計ポイント/i).first()).toBeVisible();
    await expect(page.getByText(/進行中の目標/i).first()).toBeVisible();
    await expect(page.getByText(/今週のログ/i).first()).toBeVisible();
    await expect(page.getByText(/今後のイベント/i).first()).toBeVisible();
  });

  test('クイックアクセスカードが表示される', async ({ page }) => {
    // ダッシュボードのセクション確認
    await expect(page.getByText(/進行中の目標/i).first()).toBeVisible();
    await expect(page.getByText(/最近のログ/i)).toBeVisible();
    await expect(page.getByText(/今後のイベント/i).first()).toBeVisible();
  });

  test('ナビゲーションメニューが動作する', async ({ page }) => {
    // 目標ページへ移動
    await page.getByRole('link', { name: /目標/i }).first().click();
    await expect(page).toHaveURL(/\/goals/);

    // ダッシュボードに戻る
    await page.getByRole('link', { name: /ダッシュボード/i }).first().click();
    await expect(page).toHaveURL(/\/dashboard/);
  });
});
