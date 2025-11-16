import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright E2E テスト設定
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './e2e',

  /* 並列実行の最大ワーカー数 */
  fullyParallel: true,

  /* CI環境で失敗時にリトライしない */
  forbidOnly: !!process.env.CI,

  /* CI環境でのリトライ設定 */
  retries: process.env.CI ? 2 : 0,

  /* 並列ワーカー数 */
  workers: process.env.CI ? 1 : undefined,

  /* テストレポート設定 */
  reporter: 'html',

  /* 共通設定 */
  use: {
    /* ベースURL */
    baseURL: 'http://localhost:3000',

    /* 失敗時のスクリーンショット */
    screenshot: 'only-on-failure',

    /* 失敗時のビデオ録画 */
    video: 'retain-on-failure',

    /* トレース設定 */
    trace: 'on-first-retry',
  },

  /* テスト実行前にdev serverを起動 */
  // 既にサーバーが起動している場合はコメントアウト
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120000,
  // },

  /* プロジェクト設定（ブラウザ） */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    // 必要に応じて他のブラウザも追加可能
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],
});
