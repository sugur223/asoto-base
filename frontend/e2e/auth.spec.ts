import { test, expect } from '@playwright/test';

test.describe('認証フロー', () => {
  test('ログインページが表示される', async ({ page }) => {
    await page.goto('/login');

    // ページタイトルを確認
    await expect(page).toHaveTitle(/asotobase/i);

    // ログインフォームの要素を確認
    await expect(page.getByLabel(/メールアドレス/i)).toBeVisible();
    await expect(page.getByLabel(/パスワード/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /ログイン/i })).toBeVisible();
  });

  test('新規登録ページが表示される', async ({ page }) => {
    await page.goto('/register');

    // 新規登録フォームの要素を確認
    await expect(page.getByLabel(/お名前/i)).toBeVisible();
    await expect(page.getByLabel(/メールアドレス/i)).toBeVisible();
    await expect(page.getByLabel('パスワード', { exact: true })).toBeVisible();
    await expect(page.getByLabel(/パスワード（確認）/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /登録/i })).toBeVisible();
  });

  test('ログインからダッシュボードまでの遷移', async ({ page }) => {
    // ログインページへ移動
    await page.goto('/login');

    // テストユーザーでログイン
    await page.getByLabel(/メールアドレス/i).fill('test@example.com');
    await page.getByLabel(/パスワード/i).fill('password123');
    await page.getByRole('button', { name: /ログイン/i }).click();

    // ダッシュボードへのリダイレクトを待つ
    await page.waitForURL('/dashboard', { timeout: 5000 });

    // ダッシュボードの要素を確認（heading使用）
    await expect(page.getByRole('heading', { name: /ダッシュボード/i })).toBeVisible();
  });

  test('未ログイン状態でダッシュボードにアクセスするとログインページにリダイレクト', async ({ page }) => {
    await page.goto('/dashboard');

    // ログインページにリダイレクトされることを確認（リダイレクトパラメータ付き）
    await page.waitForURL(/\/login/, { timeout: 5000 });
    await expect(page.getByRole('button', { name: /ログイン/i })).toBeVisible();
  });

  test('バリデーションエラーが表示される', async ({ page }) => {
    await page.goto('/login');

    // 空のフォームで送信
    await page.getByRole('button', { name: /ログイン/i }).click();

    // エラーメッセージが表示されることを確認（より具体的に）
    await expect(page.getByText(/有効なメールアドレスを入力してください/i)).toBeVisible();
  });
});
