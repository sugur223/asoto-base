# E2Eテスト（Playwright）

このディレクトリにはPlaywrightを使用したE2Eテストが含まれています。

## セットアップ

```bash
# 依存関係のインストール
npm install

# Playwrightブラウザのインストール
npx playwright install
```

## テストの実行

### 基本的な実行

```bash
# すべてのE2Eテストを実行
npm run test:e2e

# ヘッドレスモードで実行（ブラウザを表示）
npm run test:e2e:headed

# UIモードで実行（インタラクティブ）
npm run test:e2e:ui

# デバッグモードで実行
npm run test:e2e:debug

# テストレポートを表示
npm run test:e2e:report
```

### 特定のテストファイルを実行

```bash
# 認証テストのみ実行
npx playwright test auth.spec.ts

# ダッシュボードテストのみ実行
npx playwright test dashboard.spec.ts

# 目標管理テストのみ実行
npx playwright test goals.spec.ts
```

### 特定のブラウザで実行

```bash
# Chromiumのみ
npx playwright test --project=chromium

# Firefoxのみ
npx playwright test --project=firefox

# WebKitのみ
npx playwright test --project=webkit
```

## テストファイル構成

```
e2e/
├── README.md           # このファイル
├── fixtures.ts         # テスト用フィクスチャとヘルパー
├── auth.spec.ts        # 認証フローのテスト
├── dashboard.spec.ts   # ダッシュボードのテスト
└── goals.spec.ts       # 目標管理のテスト
```

## テストの書き方

### 基本的なテスト構造

```typescript
import { test, expect } from '@playwright/test';

test.describe('機能名', () => {
  test.beforeEach(async ({ page }) => {
    // 各テスト前の共通処理
    await page.goto('/some-page');
  });

  test('テスト名', async ({ page }) => {
    // テストロジック
    await expect(page.getByText('Expected Text')).toBeVisible();
  });
});
```

### 認証済みページのテスト

```typescript
import { test, expect } from './fixtures';

test('認証が必要なテスト', async ({ authenticatedPage }) => {
  // authenticatedPageは既にログイン済み
  await authenticatedPage.goto('/protected-page');
  await expect(authenticatedPage.getByText('Welcome')).toBeVisible();
});
```

## デバッグ

### トレースビューアー

```bash
# トレースを有効にして実行
npx playwright test --trace on

# トレースを表示
npx playwright show-trace trace.zip
```

### スクリーンショット

失敗したテストのスクリーンショットは自動的に `test-results/` ディレクトリに保存されます。

### ビデオ録画

失敗したテストのビデオは自動的に保存されます（playwright.config.tsで設定）。

## CI/CD統合

GitHub ActionsなどのCI環境では、以下のように実行できます：

```yaml
- name: Run E2E tests
  run: npm run test:e2e
```

## ベストプラクティス

1. **ページオブジェクトパターン**を使用してテストを構造化
2. **data-testid**属性を使用して要素を特定
3. **waitForURL**や**waitForSelector**を使用して非同期処理を待つ
4. **beforeEach**で共通のセットアップを行う
5. **失敗時のスクリーンショット**を活用してデバッグ

## 注意事項

- E2Eテストを実行する前に、バックエンドAPIが起動していることを確認してください
- `playwright.config.ts`の`webServer`設定により、フロントエンドは自動的に起動します
- テストデータはテスト実行後にクリーンアップされることを前提としています
