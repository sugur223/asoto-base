# システムアーキテクチャ

## 1. 全体構成

```
┌─────────────────────────────────────────────────────────┐
│                    Users / Clients                      │
│            (Web Browser / Mobile App)                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS
                     │
┌────────────────────▼────────────────────────────────────┐
│                  CDN / Load Balancer                    │
└────────────────────┬────────────────────────────────────┘
                     │
       ┌─────────────┴─────────────┐
       │                           │
┌──────▼───────┐          ┌───────▼────────┐
│   Frontend   │          │    Backend     │
│   (SPA)      │          │    (API)       │
│              │          │                │
│  - React     │          │  - Python 3.11+│
│  - Next.js   │          │  - FastAPI     │
│  - TypeScript│          │  - Pydantic    │
└──────────────┘          └───────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
          ┌─────────▼───┐  ┌──────▼──────┐  ┌──▼────────┐
          │  Database   │  │   Cache     │  │   Queue   │
          │             │  │             │  │           │
          │ PostgreSQL  │  │   Redis     │  │   Celery  │
          └─────────────┘  └─────────────┘  └───────────┘
                    │
          ┌─────────▼─────────────┐
          │  External Services    │
          │                       │
          │  - AI/ML (OpenAI)     │
          │  - Storage (S3)       │
          │  - Email (SendGrid)   │
          │  - Auth (Auth0)       │
          └───────────────────────┘
```

## 2. なぜPython + FastAPI？

### プロジェクトとの相性

| 要件 | Python + FastAPIの優位性 |
|------|------------------------|
| AI/ML機能 | OpenAI、Anthropic、scikit-learn等のライブラリが豊富 |
| データ分析 | pandas、numpyでスコア計算やマッチングアルゴリズムが容易 |
| 自然言語処理 | NLTK、spaCyなどのNLPライブラリが充実 |
| 開発速度 | Pythonの簡潔な文法で素早くプロトタイピング可能 |
| パフォーマンス | FastAPIは非常に高速（Node.jsと同等以上） |

### FastAPIの特徴

1. **非同期処理**: async/awaitネイティブサポート
2. **型安全**: Pydanticによる自動バリデーション
3. **自動ドキュメント**: Swagger UI、ReDocが自動生成
4. **高速**: Starlette + Uvicornで高パフォーマンス
5. **モダンなPython**: Python 3.7+の型ヒントを活用

## 3. バックエンド構成

### 技術スタック

| 項目 | 技術 | 理由 |
|------|------|------|
| Pythonバージョン | Python 3.11+ | 最新機能、パフォーマンス向上 |
| Webフレームワーク | FastAPI 0.104+ | 高速、型安全、自動ドキュメント |
| バリデーション | Pydantic v2 | 型チェック、データ検証 |
| ORM | SQLAlchemy 2.0+ | 強力、柔軟、非同期対応 |
| マイグレーション | Alembic | SQLAlchemyと統合 |
| 認証 | python-jose (JWT) | JWT生成・検証 |
| パスワード | passlib + bcrypt | 安全なハッシュ化 |
| 非同期DB | asyncpg | PostgreSQL非同期ドライバ |
| タスクキュー | Celery + Redis | バックグラウンド処理 |
| AI/ML | OpenAI SDK, langchain | AIコーチング実装 |
| データ分析 | pandas, numpy | スコア計算、分析 |
| テスト | pytest + pytest-asyncio | 非同期対応テスト |
| コード品質 | black, ruff, mypy | フォーマット、リント、型チェック |

### ディレクトリ構造

```
backend/
├── app/
│   ├── main.py                 # FastAPIアプリケーションエントリポイント
│   ├── config.py               # 設定管理（環境変数）
│   ├── database.py             # DB接続設定
│   │
│   ├── api/                    # APIエンドポイント
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # 認証関連
│   │   │   ├── users.py        # ユーザー管理
│   │   │   ├── steps.py        # あそとステップ
│   │   │   ├── logs.py         # 内省ログ
│   │   │   ├── events.py       # イベント
│   │   │   ├── projects.py     # プロジェクト
│   │   │   ├── matching.py     # マッチング
│   │   │   ├── coaching.py     # AIコーチング
│   │   │   └── dashboard.py    # ダッシュボード
│   │   └── deps.py             # 依存性注入
│   │
│   ├── models/                 # SQLAlchemyモデル
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── step.py
│   │   ├── log.py
│   │   ├── event.py
│   │   ├── project.py
│   │   └── coaching.py
│   │
│   ├── schemas/                # Pydanticスキーマ（リクエスト/レスポンス）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── step.py
│   │   ├── log.py
│   │   ├── event.py
│   │   └── coaching.py
│   │
│   ├── services/               # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── ai/
│   │   │   ├── coaching.py     # AIコーチングロジック
│   │   │   ├── feedback.py     # ログフィードバック生成
│   │   │   └── prompts.py      # プロンプトテンプレート
│   │   ├── matching/
│   │   │   ├── algorithm.py    # マッチングアルゴリズム
│   │   │   └── scorer.py       # スコアリング
│   │   ├── analytics/
│   │   │   ├── growth.py       # 成長分析
│   │   │   └── metrics.py      # メトリクス計算
│   │   ├── notification.py     # 通知サービス
│   │   └── points.py           # ポイント計算
│   │
│   ├── core/                   # コア機能
│   │   ├── __init__.py
│   │   ├── security.py         # セキュリティ機能（JWT等）
│   │   ├── config.py           # 設定
│   │   └── logging.py          # ロギング設定
│   │
│   ├── middleware/             # ミドルウェア
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cors.py
│   │   └── error_handler.py
│   │
│   ├── utils/                  # ユーティリティ
│   │   ├── __init__.py
│   │   ├── datetime.py
│   │   └── validators.py
│   │
│   └── tasks/                  # Celeryタスク
│       ├── __init__.py
│       ├── ai_tasks.py         # AI処理（非同期）
│       ├── notification_tasks.py
│       └── analytics_tasks.py
│
├── alembic/                    # DBマイグレーション
│   ├── versions/
│   └── env.py
│
├── tests/                      # テスト
│   ├── api/
│   ├── services/
│   └── conftest.py
│
├── scripts/                    # ユーティリティスクリプト
│   ├── seed_db.py
│   └── migrate.py
│
├── requirements.txt            # 依存パッケージ
├── requirements-dev.txt        # 開発用依存パッケージ
├── pyproject.toml              # プロジェクト設定
├── .env.example                # 環境変数サンプル
└── README.md
```

### 主要ファイルの例

#### `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, steps, logs, events, coaching
from app.core.config import settings
from app.database import engine
from app.models import Base

# テーブル作成（本番ではAlembic使用）
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="asotobase API",
    description="あそとベースのバックエンドAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(steps.router, prefix="/api/v1/steps", tags=["steps"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(coaching.router, prefix="/api/v1/coaching", tags=["coaching"])

@app.get("/")
async def root():
    return {"message": "Welcome to asotobase API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### `app/schemas/step.py`

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class StepCategory(str, Enum):
    RELATIONSHIP = "relationship"
    ACTIVITY = "activity"
    SENSITIVITY = "sensitivity"

class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class StepBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: StepCategory
    estimated_minutes: Optional[int] = Field(None, ge=0)
    due_date: Optional[datetime] = None

class StepCreate(StepBase):
    goal_id: str

class StepUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[StepStatus] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = None

class StepInDB(StepBase):
    id: str
    goal_id: str
    order: int
    status: StepStatus
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    points: Optional[int]

    class Config:
        from_attributes = True

class StepResponse(StepInDB):
    pass
```

#### `app/models/step.py`

```python
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class StepCategory(str, enum.Enum):
    RELATIONSHIP = "relationship"
    ACTIVITY = "activity"
    SENSITIVITY = "sensitivity"

class StepStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class Step(Base):
    __tablename__ = "steps"

    id = Column(String, primary_key=True)
    goal_id = Column(String, ForeignKey("goals.id"), nullable=False)
    order = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    category = Column(Enum(StepCategory), nullable=False)
    status = Column(Enum(StepStatus), default=StepStatus.PENDING)
    estimated_minutes = Column(Integer, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(String, nullable=True)
    points = Column(Integer, nullable=True)

    # Relationships
    goal = relationship("Goal", back_populates="steps")
```

#### `app/api/v1/steps.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.step import StepCreate, StepUpdate, StepResponse
from app.models.step import Step, StepStatus
from app.api.deps import get_current_user
from app.models.user import User
import uuid

router = APIRouter()

@router.get("/", response_model=List[StepResponse])
async def get_steps(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ユーザーのステップ一覧を取得"""
    # 実装は省略（SQLAlchemyのクエリ）
    pass

@router.post("/", response_model=StepResponse, status_code=status.HTTP_201_CREATED)
async def create_step(
    step: StepCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """新しいステップを作成"""
    db_step = Step(
        id=str(uuid.uuid4()),
        **step.dict(),
        order=0  # 実際は最後の順序を計算
    )
    db.add(db_step)
    await db.commit()
    await db.refresh(db_step)
    return db_step

@router.put("/{step_id}", response_model=StepResponse)
async def update_step(
    step_id: str,
    step_update: StepUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ステップを更新"""
    # 実装は省略
    pass

@router.post("/{step_id}/complete", response_model=StepResponse)
async def complete_step(
    step_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ステップを完了"""
    # 1. ステップを取得
    # 2. ステータスを完了に更新
    # 3. ポイントを付与
    # 4. 目標の進捗率を更新
    # 実装は省略
    pass

@router.delete("/{step_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_step(
    step_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ステップを削除"""
    # 実装は省略
    pass
```

#### `app/services/ai/coaching.py`

```python
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.user import User
from app.models.log import Log
from typing import List, Dict

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_log_feedback(log: Log, user: User) -> str:
    """内省ログに対するAIフィードバックを生成"""

    prompt = f"""
あなたは「あそと」コミュニティのAIコーチです。
ユーザーが投稿したログに対してフィードバックを提供します。

【ユーザー情報】
- 名前: {user.name}
- あそと3要素スコア:
  - 関係性: {user.relationship_score}/100
  - 多動性: {user.activity_score}/100
  - 感受性: {user.sensitivity_score}/100

【投稿されたログ】
タイトル: {log.title}
本文: {log.content}

【フィードバックの目的】
1. ログの内容を肯定的に受け止める
2. 気づきのポイントを明確化する
3. さらに深めるための質問を投げかける
4. 次のアクションを提案する

温かく励ましの姿勢で、具体的で実践的なフィードバックを生成してください。
"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "あなたは共感的で励ましのAIコーチです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        # エラーハンドリング
        raise Exception(f"AI feedback generation failed: {str(e)}")

async def start_coaching_session(
    user: User,
    session_type: str,
    context: Dict
) -> str:
    """AIコーチングセッションを開始"""

    # セッションタイプに応じたプロンプトを生成
    # 実装は省略
    pass

async def continue_coaching_dialogue(
    session_id: str,
    user_message: str,
    conversation_history: List[Dict]
) -> str:
    """コーチング対話を継続"""

    # 会話履歴を含めてAIに送信
    # 実装は省略
    pass
```

#### `app/services/analytics/metrics.py`

```python
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from datetime import datetime, timedelta

def normalize(value: float, min_val: float, max_val: float) -> float:
    """値を0-100に正規化"""
    if max_val == min_val:
        return 0
    return min(100, max(0, (value - min_val) / (max_val - min_val) * 100))

async def calculate_relationship_score(user: User, db: AsyncSession) -> int:
    """関係性スコアを計算"""

    # 過去30日のデータを取得
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # イベント参加数、新しいつながり、コメント数などを集計
    # 実装は省略（SQLクエリ）

    weights = {
        'event_participation': 0.3,
        'new_connections': 0.25,
        'comments': 0.2,
        'matching': 0.15,
        'event_hosting': 0.1
    }

    # 正規化して加重平均
    normalized = {
        'event_participation': normalize(event_count, 0, 10),
        'new_connections': normalize(connection_count, 0, 15),
        'comments': normalize(comment_count, 0, 20),
        'matching': normalize(matching_count, 0, 5),
        'event_hosting': normalize(hosting_count, 0, 3)
    }

    score = sum(normalized[k] * weights[k] for k in weights.keys())
    return round(score)

async def calculate_activity_score(user: User, db: AsyncSession) -> int:
    """多動性スコアを計算"""
    # 実装は省略
    pass

async def calculate_sensitivity_score(user: User, db: AsyncSession) -> int:
    """感受性スコアを計算"""
    # 実装は省略
    pass

async def update_all_scores(user: User, db: AsyncSession):
    """全スコアを更新"""
    user.relationship_score = await calculate_relationship_score(user, db)
    user.activity_score = await calculate_activity_score(user, db)
    user.sensitivity_score = await calculate_sensitivity_score(user, db)

    await db.commit()
```

## 4. 依存パッケージ

### `requirements.txt`

```
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1

# Redis
redis==5.0.1
hiredis==2.2.3

# Task Queue
celery==5.3.4

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# AI/ML
openai==1.3.5
langchain==0.0.340
tiktoken==0.5.1

# Data Analysis
pandas==2.1.3
numpy==1.26.2
scikit-learn==1.3.2

# HTTP Client
httpx==0.25.1

# Email
python-dotenv==1.0.0
emails==0.6

# Utilities
python-dateutil==2.8.2
pytz==2023.3
```

### `requirements-dev.txt`

```
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.1

# Code Quality
black==23.11.0
ruff==0.1.6
mypy==1.7.1

# Documentation
mkdocs==1.5.3
mkdocs-material==9.4.14
```

## 5. 開発環境セットアップ

### ローカル開発

```bash
# Python 3.11以上をインストール
python --version  # 3.11以上を確認

# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージインストール
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 環境変数設定
cp .env.example .env
# .env を編集

# データベースマイグレーション
alembic upgrade head

# 開発サーバー起動
uvicorn app.main:app --reload --port 8000
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/asotobase
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: asotobase
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A app.tasks worker --loglevel=info
    volumes:
      - ./app:/app
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/asotobase
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

起動コマンド：
```bash
docker-compose up -d
```

## 6. Node.js vs Python比較

| 項目 | Node.js + Express | Python + FastAPI | 勝者 |
|------|------------------|------------------|------|
| 開発速度 | 普通 | 高い（簡潔な文法） | Python |
| パフォーマンス | 高速 | 非常に高速 | 互角 |
| AI/ML統合 | ライブラリ少ない | 非常に豊富 | Python |
| データ分析 | 弱い | 非常に強い | Python |
| 型安全性 | TypeScript必須 | Pydantic標準 | 互角 |
| 自動ドキュメント | 手動またはライブラリ | 標準で完備 | Python |
| エコシステム | 巨大 | 巨大 | 互角 |
| 学習曲線 | 緩やか | 緩やか | 互角 |
| フルスタック | Next.js統合◎ | 分離必須 | Node.js |

## 7. 推奨する理由

### asotobaseにPython + FastAPIが最適な理由

1. **AIコーチング機能**: OpenAI、langchainなどのPythonライブラリが充実
2. **データ分析**: pandas、numpyでスコア計算が容易
3. **マッチングアルゴリズム**: scikit-learnで機械学習ベースのマッチングも可能
4. **自然言語処理**: ログの分析にNLPライブラリを活用できる
5. **開発速度**: Pythonの簡潔な文法で素早く実装
6. **型安全性**: Pydanticで型チェックとバリデーションが自動化
7. **ドキュメント**: Swagger UIが自動生成され、フロントエンドとの連携が容易

## 8. デプロイオプション

### 推奨構成（クラウド）

**AWS**
- **Backend**: ECS Fargate（Dockerコンテナ）
- **Database**: RDS for PostgreSQL
- **Cache**: ElastiCache for Redis
- **Storage**: S3
- **CDN**: CloudFront

**代替案（より簡単）**
- **Backend**: Render.com（Pythonアプリ対応、自動デプロイ）
- **Database**: Supabase（PostgreSQL）
- **Frontend**: Vercel

### デプロイ手順（Render.com例）

1. GitHubリポジトリにプッシュ
2. Render.comでWeb Serviceを作成
3. 環境変数を設定
4. 自動デプロイ

## 9. パフォーマンス比較

### ベンチマーク（参考値）

```
リクエスト/秒:
- FastAPI:     ~25,000 req/s
- Node.js:     ~20,000 req/s
- Django:      ~5,000 req/s

レスポンスタイム:
- FastAPI:     ~5ms
- Node.js:     ~6ms
- Django:      ~15ms
```

FastAPIは非同期処理により、Node.jsと同等以上のパフォーマンスを発揮します。

## 10. まとめ

**Python + FastAPIを採用すべき理由：**
- AIコーチング機能の実装が容易
- データ分析・マッチングアルゴリズムに強い
- 高速で型安全
- 自動ドキュメント生成
- 開発速度が速い

**Node.jsの方が良い場合：**
- フルスタックTypeScriptで統一したい
- Next.jsとの緊密な統合が必要
- AI/ML機能の重要度が低い

asotobaseの場合、AIコーチングとデータ分析が中核機能なので、**Python + FastAPIが最適**です。
