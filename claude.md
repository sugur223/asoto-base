# asotobase 開発メモ

## 変更履歴

### 2025-11-12

**アーキテクチャ変更**
- バックエンドを Node.js + Express から **Python + FastAPI** に変更
- 理由:
  - AIコーチング機能でOpenAI、langchain等のPythonライブラリが充実
  - データ分析（pandas、numpy）でスコア計算が容易
  - マッチングアルゴリズムでscikit-learn等のML活用可能
  - FastAPIは非同期処理で高速（Node.jsと同等以上）
  - Pydanticによる型安全性、自動ドキュメント生成

**削除したドキュメント**
- 旧 `docs/ARCHITECTURE.md` (Node.js版) を削除し、Python + FastAPI版に置き換え

**現在のドキュメント構成**（読む順に番号付け）
```
docs/
├── 01_CONCEPT.md                      # コンセプト・ビジョン
├── 02_FEATURES.md                     # 機能要件（概要）
├── 03_FEATURES_DETAIL_STEPS.md        # あそとステップ管理の詳細
├── 04_FEATURES_DETAIL_LOGS.md         # 内省ログ機能の詳細
├── 05_FEATURES_DETAIL_AI_COACHING.md  # AIコーチング機能の詳細
├── 06_TECH_COMPARISON.md              # 技術スタック比較・選定理由
├── 07_ARCHITECTURE.md                 # システムアーキテクチャ（Python + FastAPI）
└── 08_INFRASTRUCTURE.md               # インフラ構成・段階的移行戦略
```

**完成した詳細設計**
- ✅ あそとステップ管理機能
- ✅ 内省ログ機能
- ✅ AIコーチング機能
- ✅ マッチング機能
- ✅ イベント管理機能
- ✅ 貢献度ポイント機能
- ✅ ダッシュボード機能

## 技術スタック（確定版）

### フロントエンド
- Next.js 14+ (App Router)
- React 18+
- TypeScript
- Tailwind CSS
- shadcn/ui

### バックエンド
- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 (非同期)
- Alembic (マイグレーション)
- python-jose (JWT認証)
- passlib + bcrypt (パスワードハッシュ)

### AI/ML
- OpenAI API
- langchain
- pandas, numpy, scikit-learn

### インフラ構成（段階的移行）

#### Phase 1: MVP・開発（0-3ヶ月、〜50ユーザー）
**コスト: $0〜$10/月**

- Frontend: Vercel (無料)
- Backend: Render.com / Railway (無料〜$5/月)
- Database: Supabase PostgreSQL (無料プラン)
- Cache: Upstash Redis (無料プラン)
- Storage: Supabase Storage
- Auth: 自前JWT (python-jose)

#### Phase 2: ベータ版（3-6ヶ月、50-500ユーザー）
**コスト: $50〜$100/月**

- Frontend: Vercel (無料 or Pro)
- Backend: Render.com ($25/月)
- Database: Supabase PostgreSQL (Proプラン $25/月)
- Cache: Upstash Redis or Redis Labs
- Storage: Supabase Storage
- Auth: 自前JWT（変更なし）

#### Phase 3: 本番スケール（6ヶ月以降、500ユーザー以上）
**コスト: $200〜$500/月**

- Frontend: Vercel or CloudFront + S3
- Backend: AWS ECS Fargate
- Database: **Aurora PostgreSQL Serverless v2**
- Cache: ElastiCache for Redis
- Storage: S3
- Auth: 自前JWT（変更なし）
- Task Queue: Celery + Redis

**移行戦略**
- PostgreSQL互換のため、Supabase → Auroraはpg_dump/restoreで移行可能
- 認証を自前JWTで実装することで、Supabaseへの依存を最小化
- ストレージ層を抽象化し、Supabase Storage → S3への切り替えを容易に

## 次のステップ

1. 残りの機能詳細設計（マッチング、イベント、ポイント、ダッシュボード）
2. プロジェクト初期セットアップ
3. データベーススキーマ実装（SQLAlchemyモデル全体）
4. MVPの実装開始

## メモ

- 「あそと」= 「遊び」+「仕事」の造語
- あそと3要素: ①関係性、②多動性、③感受性
- 会社では組織性・一貫性・論理性が磨かれるため、あそとで補完する
