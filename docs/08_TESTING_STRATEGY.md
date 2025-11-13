# テスト戦略・TDD開発方針

## 基本方針

**開発スタイル**: TDD（テスト駆動開発）
- Red → Green → Refactor のサイクルを回す
- 実装前にテストを書く
- テストが通ることを確認してから次に進む

**テスト自動化**
- すべてのテストはCI/CDパイプラインで自動実行
- Pull Request時に自動テスト実行
- mainブランチへのマージ前にテストが必須

## テストレベル

### 1. 単体テスト（Unit Test）
**カバレッジ目標**: 80%以上

**バックエンド（Python + pytest）**
- モデルのバリデーション
- ビジネスロジック
- ユーティリティ関数
- ポイント計算ロジック

**フロントエンド（Jest + React Testing Library）**
- コンポーネント単体
- カスタムフック
- ユーティリティ関数

### 2. 統合テスト（Integration Test）
**カバレッジ目標**: 主要機能100%

**バックエンド**
- API エンドポイント
- データベース操作
- 認証・認可フロー

**フロントエンド**
- ページ全体の動作
- APIとの連携

### 3. E2Eテスト（End-to-End Test）
**カバレッジ目標**: 主要ユーザーフロー100%

**ツール**: Playwright

**対象フロー**
- ユーザー登録 → ログイン → ダッシュボード表示
- 目標作成 → ステップ追加 → ステップ完了 → 目標達成
- イベント作成 → イベント参加
- プロジェクト作成 → メンバー募集 → 参加リクエスト → 承認
- ログ投稿 → ログ検索

## バックエンドテスト構成

### ディレクトリ構造

```
backend/
├── app/
│   ├── models/
│   ├── api/
│   ├── core/
│   └── services/
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # pytest設定・フィクスチャ
│   ├── unit/                 # 単体テスト
│   │   ├── test_models.py
│   │   ├── test_security.py
│   │   └── test_services.py
│   ├── integration/          # 統合テスト
│   │   ├── test_auth_api.py
│   │   ├── test_goals_api.py
│   │   ├── test_logs_api.py
│   │   ├── test_events_api.py
│   │   └── test_projects_api.py
│   └── fixtures/             # テストデータ
│       ├── users.py
│       ├── goals.py
│       └── events.py
└── pytest.ini
```

### pytest設定

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
asyncio_mode = auto
```

### テストデータベース

- SQLiteをテスト用DBとして使用（高速）
- 各テスト実行前にDBをリセット
- トランザクションロールバックでクリーンアップ

### フィクスチャ例

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.main import app
from httpx import AsyncClient

# テスト用DB（SQLite）
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """イベントループのフィクスチャ"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def test_db():
    """テスト用データベース"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # テーブル作成
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # セッション作成
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # テーブル削除（クリーンアップ）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest.fixture
async def client(test_db):
    """テスト用HTTPクライアント"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def test_user(test_db):
    """テスト用ユーザー"""
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User"
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user

@pytest.fixture
async def auth_headers(test_user):
    """認証ヘッダー"""
    from app.core.security import create_access_token

    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}
```

### テスト例

#### 単体テスト例

```python
# tests/unit/test_security.py
import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)

def test_password_hashing():
    """パスワードハッシュ化のテスト"""
    password = "test_password_123"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_create_and_decode_token():
    """JWTトークン生成・検証のテスト"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    token = create_access_token(data={"sub": user_id})

    assert token is not None
    assert isinstance(token, str)

    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == user_id

def test_decode_invalid_token():
    """不正なトークンのテスト"""
    payload = decode_access_token("invalid_token")
    assert payload is None
```

#### 統合テスト例

```python
# tests/integration/test_auth_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """ユーザー登録のテスト"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user):
    """重複メールアドレスでの登録テスト"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "password123",
            "full_name": "Duplicate User"
        }
    )

    assert response.status_code == 400
    assert "既に登録されています" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user):
    """ログインのテスト"""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user):
    """間違ったパスワードでのログインテスト"""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, auth_headers):
    """現在のユーザー情報取得のテスト"""
    response = await client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
```

## フロントエンドテスト構成

### ディレクトリ構造

```
frontend/
├── src/
│   ├── components/
│   ├── app/
│   ├── lib/
│   └── __tests__/           # テスト
│       ├── unit/
│       │   ├── components/
│       │   └── lib/
│       ├── integration/
│       └── e2e/
├── jest.config.js
├── jest.setup.js
└── playwright.config.ts
```

### Jest設定

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
}
```

### テスト例

```typescript
// src/__tests__/unit/components/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { LoginForm } from '@/components/LoginForm'
import { authApi } from '@/lib/auth'

jest.mock('@/lib/auth')

describe('LoginForm', () => {
  it('正常にログインできる', async () => {
    const mockLogin = jest.fn().mockResolvedValue({
      access_token: 'test_token',
      token_type: 'bearer'
    })
    ;(authApi.login as jest.Mock) = mockLogin

    render(<LoginForm />)

    fireEvent.change(screen.getByLabelText('メールアドレス'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('パスワード'), {
      target: { value: 'password123' }
    })
    fireEvent.click(screen.getByRole('button', { name: 'ログイン' }))

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      })
    })
  })

  it('バリデーションエラーを表示', async () => {
    render(<LoginForm />)

    fireEvent.click(screen.getByRole('button', { name: 'ログイン' }))

    await waitFor(() => {
      expect(screen.getByText('メールアドレスは必須です')).toBeInTheDocument()
      expect(screen.getByText('パスワードは必須です')).toBeInTheDocument()
    })
  })
})
```

## E2Eテスト

### Playwright設定

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './src/__tests__/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### E2Eテスト例

```typescript
// src/__tests__/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('認証フロー', () => {
  test('ユーザー登録からログインまで', async ({ page }) => {
    // ユーザー登録
    await page.goto('/register')
    await page.fill('input[name="email"]', 'e2e@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.fill('input[name="full_name"]', 'E2E Test User')
    await page.click('button[type="submit"]')

    // ダッシュボードにリダイレクトされることを確認
    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('h1')).toContainText('ダッシュボード')
  })

  test('ログインエラーハンドリング', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[name="email"]', 'wrong@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    // エラーメッセージを確認
    await expect(page.locator('.error')).toContainText('メールアドレスまたはパスワードが正しくありません')
  })
})
```

## CI/CDパイプライン

### GitHub Actions設定例

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: asotobase_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  frontend-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/coverage-final.json

  e2e-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

## TDD開発フロー例

### 1. テストを書く（Red）

```python
# tests/integration/test_goals_api.py
@pytest.mark.asyncio
async def test_create_goal(client: AsyncClient, auth_headers):
    """目標作成のテスト"""
    response = await client.post(
        "/api/v1/goals",
        headers=auth_headers,
        json={
            "title": "イベントに参加する",
            "description": "今月中にイベントに参加する",
            "category": "relationship",
            "due_date": "2025-11-30"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "イベントに参加する"
    assert data["category"] == "relationship"
    assert data["progress"] == 0
```

### 2. 実装する（Green）

```python
# app/api/v1/goals.py
@router.post("/goals", response_model=GoalResponse, status_code=201)
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    goal = Goal(
        **goal_data.dict(),
        user_id=current_user.id,
        progress=0
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal
```

### 3. リファクタリング（Refactor）

コードの改善、重複削除、最適化を行う

## テスト実行コマンド

### バックエンド

```bash
# すべてのテストを実行
pytest

# カバレッジ付き
pytest --cov=app --cov-report=html

# 特定のテストファイルのみ
pytest tests/integration/test_auth_api.py

# マーカーを使った実行
pytest -m "unit"  # 単体テストのみ
pytest -m "integration"  # 統合テストのみ
```

### フロントエンド

```bash
# すべてのテストを実行
npm test

# カバレッジ付き
npm test -- --coverage

# watch モード
npm test -- --watch

# E2Eテスト
npx playwright test

# E2Eテスト（特定のブラウザ）
npx playwright test --project=chromium
```

## テストカバレッジ目標

| レイヤー | 目標カバレッジ |
|---------|--------------|
| バックエンド全体 | 80%以上 |
| モデル・ビジネスロジック | 90%以上 |
| API エンドポイント | 85%以上 |
| フロントエンドコンポーネント | 70%以上 |
| 主要ユーザーフロー（E2E） | 100% |

## 継続的改善

- 週次でカバレッジレポートをレビュー
- カバレッジが低下したら原因を特定し改善
- 新機能追加時は必ずテストも追加
- バグ修正時は再発防止のためのテストを追加
