from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

# API詳細説明
description = """
## asotobase API 🚀

あそびと仕事をつなぐプラットフォーム「asotobase」のバックエンドAPI

### あそと3要素
- **①関係性** - 人とのつながり、ネットワーキング
- **②多動性** - 主体的な行動、チャレンジ
- **③感受性** - 内省、気づき、学び

### 主な機能

#### 個人機能（多動性・感受性）
* **あそとステップ管理** - 目標を小さなステップに分解し継続を支援
* **内省ログ** - 日々の活動を振り返り、学びを記録
* **プロフィール管理** - スキル・興味関心の管理

#### コミュニティ機能（関係性）
* **イベント管理** - イベント作成・参加・管理
* **プロジェクト管理** - あそび/あそとプロジェクトの運営
* **貢献度ポイント** - コミュニティへの貢献を可視化

### 認証
ほとんどのエンドポイントはJWT認証が必要です。

1. `/api/v1/auth/register` でユーザー登録
2. `/api/v1/auth/login` でログインしてトークンを取得
3. リクエストヘッダーに `Authorization: Bearer <token>` を含める
"""

tags_metadata = [
    {
        "name": "認証",
        "description": "ユーザー登録、ログイン、認証管理",
    },
    {
        "name": "あそとステップ",
        "description": "目標とステップの管理。目標を小さなステップに分解して達成を支援します。",
    },
    {
        "name": "内省ログ",
        "description": "日々の活動の振り返りログ。公開/非公開設定が可能です。",
    },
    {
        "name": "イベント",
        "description": "イベントの作成・参加・管理。オンライン/オフラインのイベントに対応。",
    },
    {
        "name": "プロジェクト",
        "description": "継続的なプロジェクトの管理。あそびプロジェクトとあそとプロジェクトの2種類。",
    },
    {
        "name": "プロフィール",
        "description": "ユーザープロフィール、スキル、興味関心の管理。",
    },
    {
        "name": "ポイント",
        "description": "貢献度ポイントの確認。活動に応じてポイントが付与されます。",
    },
    {
        "name": "ダッシュボード",
        "description": "個人とコミュニティの全体像を表示。",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="0.1.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "asotobase",
        "url": "https://github.com/asotobase/asotobase",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "Welcome to asotobase API",
        "docs": "/docs",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
