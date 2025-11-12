# インフラ構成・移行戦略

## 1. 段階的移行アプローチ

asotobaseは、**Supabase（開発・ベータ）→ Aurora（本番スケール）** の段階的な移行戦略を採用します。

### なぜ段階的移行？

1. **開発速度優先**: 最初は素早くMVPを作成
2. **コスト最適化**: 初期は無料〜低コストで運用
3. **リスク分散**: 小さく始めて段階的にスケール
4. **移行容易性**: PostgreSQL互換のため移行が簡単

## 2. Phase 1: MVP・開発（0-3ヶ月）

### 対象ユーザー
- 初期ユーザー: 〜50人
- 主に「あそと」コミュニティメンバー
- アーリーアダプター向けベータテスト

### インフラ構成

```
┌─────────────────────────────────────────┐
│           Users (Web Browser)           │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼────────┐
│   Vercel       │   │  Render.com     │
│  (Next.js)     │   │  (FastAPI)      │
│   FREE         │   │  FREE or $5/mo  │
└────────────────┘   └────────┬────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼──────┐   ┌────────▼────────┐
            │  Supabase    │   │  Upstash Redis  │
            │  PostgreSQL  │   │   (Cache)       │
            │   FREE       │   │   FREE          │
            └──────────────┘   └─────────────────┘
                    │
            ┌───────▼──────┐
            │  Supabase    │
            │   Storage    │
            │   FREE       │
            └──────────────┘
```

### 技術スタック

| コンポーネント | サービス | プラン | コスト |
|--------------|---------|-------|--------|
| Frontend | Vercel | Hobby | $0 |
| Backend | Render.com | Free | $0 |
| Database | Supabase | Free | $0 |
| Cache | Upstash Redis | Free | $0 |
| Storage | Supabase Storage | Free | $0 |
| **合計** | - | - | **$0/月** |

### Supabaseの無料プラン制限

- Database: 500MB
- Storage: 1GB
- Bandwidth: 5GB/月
- API Requests: 50,000/月

→ 50ユーザーなら十分

### セットアップ手順

#### 1. Supabaseプロジェクト作成

```bash
# 1. https://supabase.com でプロジェクト作成
# 2. Database URLを取得
# 例: postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
```

#### 2. バックエンドのデプロイ（Render.com）

```bash
# 1. GitHubリポジトリにプッシュ
git push origin main

# 2. Render.comでWeb Service作成
# - Runtime: Python 3.11
# - Build Command: pip install -r requirements.txt
# - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 3. 環境変数設定
DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
REDIS_URL=redis://[UPSTASH_URL]
OPENAI_API_KEY=sk-...
SECRET_KEY=[ランダムな文字列]
```

#### 3. フロントエンドのデプロイ（Vercel）

```bash
# Vercel CLIでデプロイ
npm install -g vercel
vercel

# または、GitHubと連携して自動デプロイ
```

### 初期マイグレーション

```bash
# ローカルでマイグレーション作成
alembic revision --autogenerate -m "Initial schema"

# Supabaseに適用
alembic upgrade head
```

## 3. Phase 2: ベータ版（3-6ヶ月）

### 対象ユーザー
- 50-500人
- 一般公開ベータ
- フィードバック収集期間

### インフラ構成（Phase 1との差分）

```
変更点:
- Render.com: Free → Starter ($25/月)
- Supabase: Free → Pro ($25/月)
- Upstash Redis: Free → Standard (必要に応じて)
```

### コスト

| コンポーネント | プラン | コスト |
|--------------|-------|--------|
| Frontend | Vercel Hobby | $0 |
| Backend | Render Starter | $25 |
| Database | Supabase Pro | $25 |
| Cache | Upstash (適宜) | $0-10 |
| **合計** | - | **$50-60/月** |

### Supabase Proプランの拡張

- Database: 8GB
- Storage: 100GB
- Bandwidth: 50GB/月
- API Requests: 500,000/月
- 自動バックアップ: 7日間
- ポイントインタイムリカバリ

### スケーリングのサイン

以下が見えたらPhase 3への移行を検討：

1. **パフォーマンス低下**
   - API応答時間が500ms超える
   - データベースクエリが遅い

2. **リソース不足**
   - Database容量が8GBの80%超え
   - API Requestsが月間上限に近づく

3. **ユーザー数増加**
   - アクティブユーザー500人突破
   - 月間PV 10万超え

## 4. Phase 3: 本番スケール（6ヶ月以降）

### 対象ユーザー
- 500人以上
- 本格的な運用フェーズ
- 高可用性・高パフォーマンス要求

### インフラ構成（AWS）

```
┌──────────────────────────────────────────────┐
│              CloudFront (CDN)                │
└─────────────┬────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼──────────┐  ┌─────▼────────────────┐
│   S3         │  │  ALB                 │
│ (Static)     │  │  (Load Balancer)     │
└──────────────┘  └─────┬────────────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
        ┌─────▼─────┐      ┌──────▼──────┐
        │  ECS      │      │  ECS        │
        │ Fargate   │      │  Fargate    │
        │ (FastAPI) │      │  (FastAPI)  │
        └─────┬─────┘      └──────┬──────┘
              │                   │
              └─────────┬─────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
    ┌─────▼──────┐ ┌────▼────┐ ┌─────▼─────┐
    │  Aurora    │ │ElastiCache│ │    S3    │
    │ PostgreSQL │ │  (Redis)  │ │ (Storage)│
    │ Serverless │ │           │ │          │
    └────────────┘ └───────────┘ └──────────┘
```

### 技術スタック

| コンポーネント | サービス | 想定コスト |
|--------------|---------|----------|
| Frontend | Vercel Pro or CloudFront + S3 | $20-50 |
| Backend | ECS Fargate (2 tasks) | $100-150 |
| Database | Aurora Serverless v2 | $80-200 |
| Cache | ElastiCache for Redis | $30-50 |
| Storage | S3 | $10-20 |
| その他（監視等） | CloudWatch, etc | $20-30 |
| **合計** | - | **$260-500/月** |

### Aurora Serverless v2の設定

```yaml
Engine: aurora-postgresql
Version: 15.3以上
Capacity:
  MinACU: 0.5  # 最小（深夜など）
  MaxACU: 4.0  # 最大（ピーク時）
Autoscaling: Enabled
MultiAZ: Enabled  # 高可用性
BackupRetention: 7 days
```

**Aurora Serverless v2のメリット**
- 自動スケーリング（0.5 ACU 〜 128 ACU）
- 使った分だけ課金（アイドル時は最小料金）
- 高速スケールアップ（数秒）
- 高可用性（マルチAZ）

## 5. データベース移行手順（Supabase → Aurora）

### 移行前の準備

#### 1. Auroraクラスター作成

```bash
# AWS CLIでAuroraクラスター作成
aws rds create-db-cluster \
  --db-cluster-identifier asotobase-cluster \
  --engine aurora-postgresql \
  --engine-version 15.3 \
  --master-username postgres \
  --master-user-password [PASSWORD] \
  --db-subnet-group-name [SUBNET_GROUP] \
  --vpc-security-group-ids [SECURITY_GROUP]

# Serverless v2インスタンス作成
aws rds create-db-instance \
  --db-instance-identifier asotobase-instance-1 \
  --db-cluster-identifier asotobase-cluster \
  --db-instance-class db.serverless \
  --engine aurora-postgresql
```

#### 2. セキュリティグループ設定

```
Inbound Rules:
- Type: PostgreSQL
- Port: 5432
- Source: [Backend ECS Security Group]
```

### 移行実施

#### ステップ1: データダンプ（Supabase）

```bash
# Supabaseからデータをダンプ
pg_dump "postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres" \
  --no-owner \
  --no-acl \
  --clean \
  --if-exists \
  > supabase_dump.sql
```

#### ステップ2: データリストア（Aurora）

```bash
# Auroraにデータをリストア
psql "postgresql://postgres:[PASSWORD]@asotobase-cluster.cluster-xxx.ap-northeast-1.rds.amazonaws.com:5432/postgres" \
  < supabase_dump.sql
```

#### ステップ3: 動作確認

```bash
# ローカルで接続テスト
export DATABASE_URL="postgresql+asyncpg://postgres:[PASSWORD]@asotobase-cluster.cluster-xxx.ap-northeast-1.rds.amazonaws.com:5432/postgres"

# マイグレーション確認
alembic current

# テストデータ取得
python scripts/test_connection.py
```

#### ステップ4: 本番切り替え

```bash
# 1. メンテナンスモード有効化（ユーザーに通知）
# 2. 最終データ同期（差分のみ）
# 3. 環境変数を更新（Render.com / ECS）
DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@asotobase-cluster...

# 4. アプリケーション再起動
# 5. 動作確認
# 6. メンテナンスモード解除
```

### ロールバックプラン

問題が発生した場合、即座にSupabaseに戻せるよう：

1. Supabaseのデータベースは削除せず、読み取り専用として保持
2. 環境変数を戻すだけでロールバック可能
3. DNSを使った段階的な切り替えも可

## 6. ストレージ移行（Supabase Storage → S3）

### コードの抽象化

```python
# app/services/storage.py
from abc import ABC, abstractmethod
from typing import BinaryIO
import boto3
from supabase import create_client

class StorageService(ABC):
    @abstractmethod
    async def upload(self, bucket: str, path: str, file: BinaryIO) -> str:
        """ファイルをアップロードし、URLを返す"""
        pass

    @abstractmethod
    async def download(self, bucket: str, path: str) -> bytes:
        """ファイルをダウンロード"""
        pass

    @abstractmethod
    async def delete(self, bucket: str, path: str) -> bool:
        """ファイルを削除"""
        pass

class SupabaseStorage(StorageService):
    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)

    async def upload(self, bucket: str, path: str, file: BinaryIO) -> str:
        result = self.client.storage.from_(bucket).upload(path, file)
        return self.client.storage.from_(bucket).get_public_url(path)

class S3Storage(StorageService):
    def __init__(self, bucket: str, region: str):
        self.s3 = boto3.client('s3', region_name=region)
        self.bucket = bucket

    async def upload(self, bucket: str, path: str, file: BinaryIO) -> str:
        self.s3.upload_fileobj(file, self.bucket, path)
        return f"https://{self.bucket}.s3.amazonaws.com/{path}"

# app/core/config.py
from app.core.config import settings

def get_storage_service() -> StorageService:
    if settings.STORAGE_PROVIDER == "supabase":
        return SupabaseStorage(
            url=settings.SUPABASE_URL,
            key=settings.SUPABASE_KEY
        )
    else:
        return S3Storage(
            bucket=settings.S3_BUCKET,
            region=settings.AWS_REGION
        )
```

### 使用例

```python
# app/api/v1/users.py
from fastapi import APIRouter, UploadFile
from app.services.storage import get_storage_service

router = APIRouter()

@router.post("/users/me/avatar")
async def upload_avatar(file: UploadFile):
    storage = get_storage_service()

    # Supabase or S3、どちらでも同じコード
    url = await storage.upload(
        bucket="avatars",
        path=f"users/{user.id}/avatar.jpg",
        file=file.file
    )

    return {"avatar_url": url}
```

### 移行時の切り替え

```bash
# 環境変数を変更するだけ
STORAGE_PROVIDER=s3  # supabase → s3
S3_BUCKET=asotobase-storage
AWS_REGION=ap-northeast-1
```

## 7. 認証実装（自前JWT）

Supabase Authは使わず、最初から自前JWT実装を推奨。

```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your-secret-key-here"  # 環境変数から読み込み
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # データベースからユーザーを取得
    # ... (省略)

    return user
```

この実装なら、**Supabase → Aurora移行時も変更不要**。

## 8. コスト削減のTips

### Phase 1-2での節約術

1. **Vercel Hobby継続使用**
   - 商用利用でもHobbyプランで問題なし（規約確認）
   - 帯域制限に注意

2. **Render.com無料枠活用**
   - 15分間アイドルでスリープ（起動に数秒）
   - ユーザーが少ないうちは許容範囲

3. **Supabase無料プランの最大活用**
   - 500MBまで無料
   - 画像は圧縮してから保存

4. **Upstash Redisの無料枠**
   - 10,000コマンド/日まで無料
   - セッション管理程度なら十分

### Phase 3でのコスト最適化

1. **Aurora Serverless v2の最小ACU調整**
   - 深夜は0.5 ACU（$0.12/時間）
   - 昼間のピークのみスケール

2. **S3のライフサイクルポリシー**
   - 30日後にIA（低頻度アクセス）へ移行
   - 90日後にGlacier（アーカイブ）へ

3. **CloudFrontのキャッシュ最適化**
   - TTL設定で帯域削減

4. **リザーブドインスタンス**
   - 1年契約で30-40%割引（確実に使う場合）

## 9. 監視・アラート

### Phase 1-2

- Render.comの標準メトリクス
- Supabaseダッシュボード
- Sentry（エラートラッキング、無料枠あり）

### Phase 3

- **CloudWatch**
  - メトリクス: CPU、メモリ、レスポンスタイム
  - アラーム: エラー率、レスポンス遅延

- **Datadog**（オプション）
  - APM（Application Performance Monitoring）
  - より詳細な分析

## 10. まとめ

### 推奨戦略

✅ **Phase 1で素早くMVP作成**（Supabase）
✅ **Phase 2でベータ運用**（Supabase Pro）
✅ **Phase 3で本番スケール**（Aurora）

### 重要なポイント

1. **認証は最初から自前JWT** → 移行容易
2. **ストレージは抽象化** → Supabase Storage/S3切り替え容易
3. **PostgreSQL互換** → Supabase/Aurora間の移行容易
4. **段階的移行** → リスク分散、コスト最適化

この戦略により、**初期コスト$0で始めて、スケールに応じて最適化**できます。
