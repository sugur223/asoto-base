# API仕様・テスト結果の確認ガイド

## API仕様の確認

FastAPIは自動的にインタラクティブなAPI仕様書を生成します。

### 1. Swagger UI（推奨）

**URL**: http://localhost:8000/docs

**特徴**:
- インタラクティブにAPIを試せる
- リクエスト/レスポンスの例が見られる
- 認証トークンを設定してAPIを実行可能
- リアルタイムでAPIをテスト

**使い方**:
1. サーバーを起動: `docker-compose up`
2. ブラウザで http://localhost:8000/docs を開く
3. エンドポイントをクリックして詳細を表示
4. 「Try it out」ボタンでAPIを実際に実行

**認証が必要なエンドポイントの場合**:
1. まず `/api/v1/auth/login` でログイン
2. レスポンスから `access_token` をコピー
3. 画面右上の「Authorize」ボタンをクリック
4. `Bearer <token>` の形式でトークンを入力
5. 以降、認証が必要なエンドポイントが実行可能に

### 2. ReDoc（ドキュメント重視）

**URL**: http://localhost:8000/redoc

**特徴**:
- 読みやすいドキュメント形式
- PDFエクスポート可能
- 検索機能あり
- モバイルフレンドリー

### 3. OpenAPI JSON

**URL**: http://localhost:8000/openapi.json

**特徴**:
- OpenAPI 3.0 仕様のJSON形式
- 他のツール（Postman、Insomnia等）にインポート可能
- CI/CDでのスキーマ検証に使用可能

## テスト結果の確認

### 1. バックエンドテスト

#### HTMLレポート（最も見やすい）

```bash
cd backend
pytest

# テスト完了後、以下のファイルが生成される
# test-report.html - テスト結果レポート
# htmlcov/index.html - カバレッジレポート
```

**test-report.html を開く**:
- テスト結果の一覧
- 成功/失敗の詳細
- エラーメッセージ
- 実行時間

**htmlcov/index.html を開く**:
- コードカバレッジの詳細
- ファイルごとのカバレッジ率
- カバーされていない行のハイライト
- 関数ごとのカバレッジ

#### ターミナル出力

```bash
# 詳細な出力
pytest -v

# カバレッジ付き
pytest --cov=app --cov-report=term-missing

# 特定のテストのみ
pytest tests/integration/test_auth_api.py -v

# マーカーで絞り込み
pytest -m unit  # 単体テストのみ
pytest -m integration  # 統合テストのみ
```

#### CI/CDでの確認

GitHub Actionsで自動実行されたテスト結果は以下で確認:
1. GitHub リポジトリの「Actions」タブ
2. 該当のワークフロー実行を選択
3. 「backend-test」ジョブを展開
4. 「Run tests」ステップでテスト結果を確認

Codecovでカバレッジを確認:
- https://codecov.io/gh/YOUR_ORG/YOUR_REPO
- Pull Requestにカバレッジレポートがコメントされる

### 2. フロントエンドテスト

```bash
cd frontend
npm test -- --coverage

# テスト完了後、以下が生成される
# coverage/lcov-report/index.html - カバレッジレポート
```

**coverage/lcov-report/index.html を開く**:
- コンポーネントごとのカバレッジ
- 関数・行・ブランチのカバレッジ率
- カバーされていないコードのハイライト

### 3. E2Eテスト

```bash
npx playwright test

# テスト完了後
npx playwright show-report
```

**Playwrightレポート**:
- ブラウザで自動的に開く
- テストの実行結果
- スクリーンショット
- 実行トレース

## 開発フロー例

### 1. 新しいAPIエンドポイントを追加

```bash
# 1. テストを書く（TDD）
vim backend/tests/integration/test_goals_api.py

# 2. テストを実行（Red）
pytest tests/integration/test_goals_api.py

# 3. 実装する
vim backend/app/api/v1/goals.py

# 4. テストを実行（Green）
pytest tests/integration/test_goals_api.py

# 5. リファクタリング
# コードを改善

# 6. Swagger UIで動作確認
# http://localhost:8000/docs を開いて実際に試す

# 7. カバレッジを確認
pytest --cov=app --cov-report=html
open htmlcov/index.html  # macOS
# または
xdg-open htmlcov/index.html  # Linux
```

### 2. Pull Request前のチェック

```bash
# すべてのテストを実行
cd backend && pytest
cd ../frontend && npm test

# カバレッジ確認
cd backend && pytest --cov=app --cov-report=term
cd ../frontend && npm test -- --coverage

# Lint チェック
cd frontend && npm run lint
```

## トラブルシューティング

### テストが失敗する

```bash
# 詳細なエラー情報を表示
pytest -vv --tb=long

# 特定のテストのみデバッグ
pytest tests/integration/test_auth_api.py::test_login -vv
```

### カバレッジが低い

```bash
# カバーされていない行を確認
pytest --cov=app --cov-report=term-missing

# HTMLレポートで詳細確認
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Swagger UIでAPIが動かない

1. サーバーが起動しているか確認: `docker-compose ps`
2. ログを確認: `docker-compose logs backend`
3. 認証が必要な場合、トークンを設定しているか確認
4. ブラウザのコンソールでエラーを確認

## ベストプラクティス

### API仕様書

- エンドポイントには必ず `summary` と `description` を付ける
- レスポンスの例（`examples`）を提供する
- エラーレスポンス（`responses`）を明示する
- タグ（`tags`）でエンドポイントをグルーピング

### テスト

- テスト名は日本語で明確に（例: `test_ユーザー登録_成功`）
- 1つのテストで1つのことだけテスト
- モックは最小限に、実際のDBを使う
- エッジケースもテスト（空文字、null、境界値）
- 失敗時のエラーメッセージも確認

### カバレッジ

- 80%以上を目標に
- 重要なビジネスロジックは100%
- カバレッジが目的ではなく、品質向上が目的
- テストしにくいコードは設計を見直す

## 参考リンク

- [FastAPI - First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI - OpenAPI](https://fastapi.tiangolo.com/tutorial/metadata/)
- [pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
