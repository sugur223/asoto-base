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
├── 01_CONCEPT.md                   # コンセプト・ビジョン
├── 02_FEATURES.md                  # 機能要件（概要）
├── 03_TECH_COMPARISON.md           # 技術スタック比較・選定理由
├── 04_ARCHITECTURE.md              # システムアーキテクチャ（Python + FastAPI）
├── 05_INFRASTRUCTURE.md            # インフラ構成・段階的移行戦略
├── 06_MVP_PLAN.md                  # MVP実装計画
├── 07_DATABASE_SCHEMA.md           # データベーススキーマ設計
├── 08_TESTING_STRATEGY.md          # テスト戦略・TDD開発方針
├── 09_API_TESTING_GUIDE.md         # API仕様・テスト実行ガイド
└── features-detail/                # 機能詳細設計（まとめ）
    ├── 01_STEPS.md                 # あそとステップ管理
    ├── 02_LOGS.md                  # 内省ログ
    ├── 03_AI_COACHING.md           # AIコーチング
    ├── 04_MATCHING.md              # マッチング
    ├── 05_EVENTS_POINTS_DASHBOARD.md  # イベント・ポイント・ダッシュボード
    └── 06_PROJECTS.md              # プロジェクト管理
```

**完成した詳細設計**
- ✅ あそとステップ管理機能
- ✅ 内省ログ機能
- ✅ AIコーチング機能
- ✅ マッチング機能（人×人、人×プロジェクト、人×イベント）
- ✅ プロジェクト管理機能（あそびプロジェクト・あそとプロジェクト）
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

## 開発の進捗状況

### ✅ 完了
- プロジェクト初期セットアップ（backend, frontend, Docker Compose）
- データベーススキーマ設計（Phase 1の全11テーブル）
- SQLAlchemyモデル実装（全11テーブル）
- Alembicマイグレーション作成・実行
- 基本的な認証API実装（register, login, me）
- テスト環境セットアップ（pytest, CI/CD）
- API仕様書（Swagger UI）

### 🔄 進行中
- Phase 1のPydantic Schemas実装
- サンプルデータスクリプト作成

### 📋 次のステップ
1. Phase 1の全スキーマを作成（goals, steps, logs, events, projects など）
2. サンプルデータスクリプト作成
3. あそとステップ管理API実装（TDD）
4. 内省ログAPI実装（TDD）
5. イベント管理API実装（TDD）
6. プロジェクト管理API実装（TDD）
7. ダッシュボードAPI実装
8. ポイントシステム実装

## メモ

- 「あそと」= 「あそび」+「仕事」の造語
- あそと3要素: ①関係性、②多動性、③感受性
- 会社では組織性・一貫性・論理性が磨かれるため、あそとで補完する

## プロジェクトとイベントの違い

- **イベント**: 日時が決まった単発の集まり（牧場見学、わいわい交流会、週末食堂など）
- **プロジェクト**: 継続的な活動
  - 🔍 **あそびプロジェクト**: 軽めの取り組み（あそとPR、哲学カフェ、AIで遊ぶ会など）
  - 🌱 **あそとプロジェクト**: 本格的な活動（クラファン、新百姓プロジェクト、サービス開発など）
