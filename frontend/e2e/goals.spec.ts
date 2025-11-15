import { test, expect } from '@playwright/test';

// テストユーザーでログインするヘルパー関数
async function login(page: any) {
  await page.goto('/login');
  await page.getByLabel(/メールアドレス/i).fill('test@example.com');
  await page.getByLabel(/パスワード/i).fill('password123');
  await page.getByRole('button', { name: /ログイン/i }).click();
  await page.waitForURL('/dashboard', { timeout: 5000 });
}

test.describe('目標管理（Goals）', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await page.goto('/goals');
  });

  test('目標一覧ページが表示される', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /目標管理/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /新しい目標を作成/i })).toBeVisible();
  });

  test('新しい目標を作成できる', async ({ page }) => {
    // 新規作成ボタンをクリック
    await page.getByRole('button', { name: /新しい目標を作成/i }).click();

    // フォームが表示されることを確認
    await expect(page.getByLabel(/タイトル/i)).toBeVisible();

    // 目標を入力
    await page.getByLabel(/タイトル/i).fill('E2Eテスト目標');

    // カテゴリを選択（存在する場合）
    const categorySelect = page.getByLabel(/カテゴリ/i);
    if (await categorySelect.isVisible()) {
      await categorySelect.selectOption('activity');
    }

    // 保存ボタンをクリック
    await page.getByRole('button', { name: /保存|作成/i }).click();

    // 目標が一覧に表示されることを確認
    await expect(page.getByText('E2Eテスト目標')).toBeVisible();
  });

  test('目標の詳細を表示できる', async ({ page }) => {
    // 既存の目標をクリック（存在する場合）
    const goalItem = page.locator('[data-testid="goal-item"]').first();

    if (await goalItem.isVisible()) {
      await goalItem.click();

      // 詳細ページに遷移
      await expect(page).toHaveURL(/\/goals\/[a-f0-9-]+/);

      // ステップ管理セクションが表示されることを確認
      await expect(page.getByText(/ステップ/i)).toBeVisible();
    }
  });

  test('フィルターが動作する', async ({ page }) => {
    // カテゴリフィルター（存在する場合）
    const filterButton = page.getByRole('button', { name: /フィルター/i });

    if (await filterButton.isVisible()) {
      await filterButton.click();

      // フィルターオプションが表示されることを確認
      await expect(page.getByText(/カテゴリ/i)).toBeVisible();
    }
  });
});
