import { test as base } from '@playwright/test';

// テスト用のユーザー情報
export const testUser = {
  email: 'test@example.com',
  password: 'password123',
  fullName: 'テストユーザー',
};

// カスタムフィクスチャ
type Fixtures = {
  authenticatedPage: any;
};

// 認証済みページのフィクスチャ
export const test = base.extend<Fixtures>({
  authenticatedPage: async ({ page }, use) => {
    // ログイン処理
    await page.goto('/login');
    await page.getByLabel(/メールアドレス/i).fill(testUser.email);
    await page.getByLabel(/パスワード/i).fill(testUser.password);
    await page.getByRole('button', { name: /ログイン/i }).click();

    // ダッシュボードへのリダイレクトを待つ
    await page.waitForURL('/dashboard', { timeout: 5000 });

    // テストに認証済みページを提供
    await use(page);
  },
});

export { expect } from '@playwright/test';
