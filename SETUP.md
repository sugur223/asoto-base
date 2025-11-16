# asotobase 開発環境セットアップ

## 必要な環境

- Docker & Docker Compose
- Git

## クイックスタート

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd asoto-base
```

### 2. 環境変数ファイルの準備

サンプルファイルから環境変数ファイルを作成します。

```bash
# バックエンド環境変数をコピー
cp backend/.env.example backend/.env

# フロントエンド環境変数をコピー
cp frontend/.env.local.example frontend/.env.local
```

開発環境ではデフォルト値で動作しますが、本番環境では必ず `backend/.env` の `SECRET_KEY` を変更してください。

### 3. Docker Composeでサービスを起動

```bash
docker-compose up -d
```

初回起動時は、イメージのビルドに時間がかかります。

### 4. データベースマイグレーション

```bash
# バックエンドコンテナに入る
docker-compose exec backend bash

# マイグレーション生成
alembic revision --autogenerate -m "Initial migration"

# マイグレーション実行
alembic upgrade head

# コンテナから出る
exit
```

### 5. アクセス確認

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

## 開発フロー

### ログ確認

```bash
# 全サービスのログ
docker-compose logs -f

# バックエンドのみ
docker-compose logs -f backend

# フロントエンドのみ
docker-compose logs -f frontend
```

### サービス再起動

```bash
# 全サービス
docker-compose restart

# 特定のサービス
docker-compose restart backend
```

### サービス停止

```bash
docker-compose down
```

### データベースリセット

```bash
# データベースのボリュームも削除
docker-compose down -v
```

## ローカル開発（Dockerなし）

### バックエンド

```bash
cd backend

# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定（.envファイルを編集）
# DATABASE_URLをローカルのPostgreSQLに変更

# マイグレーション実行
alembic upgrade head

# サーバー起動
uvicorn app.main:app --reload --port 8000
```

### フロントエンド

```bash
cd frontend

# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev
```

## プロジェクト構成

```
asoto-base/
├── backend/              # FastAPI バックエンド
│   ├── app/
│   │   ├── api/          # APIエンドポイント
│   │   ├── core/         # 設定、認証、DB
│   │   ├── models/       # SQLAlchemyモデル
│   │   ├── schemas/      # Pydanticスキーマ
│   │   └── main.py       # エントリーポイント
│   ├── alembic/          # マイグレーション
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/             # Next.js フロントエンド
│   ├── src/
│   │   ├── app/          # App Router
│   │   ├── components/   # Reactコンポーネント
│   │   ├── lib/          # ユーティリティ
│   │   └── types/        # TypeScript型定義
│   ├── package.json
│   └── Dockerfile
│
├── docs/                 # ドキュメント
├── docker-compose.yml
└── README.md
```

## API エンドポイント

### 認証

- `POST /api/v1/auth/register` - ユーザー登録
- `POST /api/v1/auth/login` - ログイン
- `GET /api/v1/auth/me` - 現在のユーザー情報取得

詳細は http://localhost:8000/docs を参照してください。

## トラブルシューティング

### ポートが既に使用されている

```bash
# ポート使用状況確認
lsof -i :3000
lsof -i :8000
lsof -i :5432

# docker-compose.ymlのポート番号を変更
```

### データベース接続エラー

```bash
# データベースコンテナの状態確認
docker-compose ps

# データベースログ確認
docker-compose logs db

# データベースコンテナ再起動
docker-compose restart db
```

### マイグレーションエラー

```bash
# マイグレーション履歴確認
docker-compose exec backend alembic current

# マイグレーションを最新に
docker-compose exec backend alembic upgrade head

# マイグレーションをリセット（注意：データが消えます）
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head
```

## 次のステップ

1. ユーザー登録・ログイン画面の実装
2. あそとステップ管理機能の実装
3. 内省ログ機能の実装

詳細は `docs/` ディレクトリのドキュメントを参照してください。
