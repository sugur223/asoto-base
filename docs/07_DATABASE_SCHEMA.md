# データベーススキーマ設計（Phase 1 MVP）

## テーブル一覧

Phase 1で実装する11個のテーブル：

1. **users** - ユーザー基本情報
2. **user_profiles** - ユーザー拡張プロフィール
3. **goals** - あそとステップの目標
4. **steps** - 目標のステップ
5. **logs** - 内省ログ
6. **events** - イベント
7. **event_participants** - イベント参加者
8. **projects** - プロジェクト
9. **project_members** - プロジェクトメンバー
10. **project_tasks** - プロジェクトタスク
11. **points** - 貢献度ポイント履歴

## ER図

```
┌─────────────┐
│   users     │
├─────────────┤
│ id (PK)     │
│ email       │
│ password    │
│ full_name   │
│ is_active   │
│ role        │
│ created_at  │
│ updated_at  │
└─────────────┘
       │
       │ 1:1
       ↓
┌──────────────────┐
│  user_profiles   │
├──────────────────┤
│ id (PK)          │
│ user_id (FK)     │◄─────┐
│ bio              │      │
│ avatar_url       │      │
│ skills (JSON)    │      │
│ interests (JSON) │      │
│ created_at       │      │
│ updated_at       │      │
└──────────────────┘      │
                          │
       ┌──────────────────┘
       │
       │ 1:N
       ↓
┌─────────────┐
│   goals     │
├─────────────┤
│ id (PK)     │
│ user_id (FK)│
│ title       │
│ description │
│ category    │
│ status      │
│ progress    │
│ due_date    │
│ completed_at│
│ created_at  │
│ updated_at  │
└─────────────┘
       │
       │ 1:N
       ↓
┌─────────────┐
│   steps     │
├─────────────┤
│ id (PK)     │
│ goal_id (FK)│
│ order       │
│ title       │
│ description │
│ status      │
│ due_date    │
│ completed_at│
│ created_at  │
│ updated_at  │
└─────────────┘

┌─────────────┐
│    logs     │
├─────────────┤
│ id (PK)     │
│ user_id (FK)│───────┐
│ title       │       │
│ content     │       │
│ tags (JSON) │       │
│ visibility  │       │
│ created_at  │       │
│ updated_at  │       │
└─────────────┘       │
                      │
┌─────────────┐       │
│   events    │       │
├─────────────┤       │
│ id (PK)     │       │
│ owner_id(FK)│───────┤
│ title       │       │
│ description │       │
│ start_date  │       │
│ end_date    │       │
│ location    │       │
│ max_attendee│       │
│ tags (JSON) │       │
│ created_at  │       │
│ updated_at  │       │
└─────────────┘       │
       │              │
       │ N:N          │
       ↓              │
┌──────────────────┐  │
│event_participants│  │
├──────────────────┤  │
│ id (PK)          │  │
│ event_id (FK)    │  │
│ user_id (FK)     │──┘
│ status           │
│ joined_at        │
│ created_at       │
└──────────────────┘

┌─────────────┐
│  projects   │
├─────────────┤
│ id (PK)     │
│ owner_id(FK)│───────┐
│ title       │       │
│ description │       │
│ category    │       │
│ status      │       │
│ start_date  │       │
│ end_date    │       │
│ location    │       │
│ is_recruiting│      │
│ max_members │       │
│ tags (JSON) │       │
│ created_at  │       │
│ updated_at  │       │
└─────────────┘       │
       │              │
       │ N:N          │
       ↓              │
┌──────────────────┐  │
│ project_members  │  │
├──────────────────┤  │
│ id (PK)          │  │
│ project_id (FK)  │  │
│ user_id (FK)     │──┘
│ role             │
│ status           │
│ contribution_pts │
│ joined_at        │
│ created_at       │
└──────────────────┘

┌─────────────┐
│project_tasks│
├─────────────┤
│ id (PK)     │
│ project_id  │
│ assignee_id │
│ title       │
│ description │
│ status      │
│ order       │
│ due_date    │
│ completed_at│
│ created_at  │
│ updated_at  │
└─────────────┘

┌─────────────┐
│   points    │
├─────────────┤
│ id (PK)     │
│ user_id (FK)│
│ amount      │
│ action_type │
│ reference_id│
│ description │
│ created_at  │
└─────────────┘
```

## テーブル詳細設計

### 1. users（ユーザー）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | ユーザーID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | メールアドレス |
| hashed_password | VARCHAR(255) | NOT NULL | ハッシュ化されたパスワード |
| full_name | VARCHAR(255) | | 氏名 |
| is_active | BOOLEAN | DEFAULT TRUE | アクティブフラグ |
| role | ENUM | DEFAULT 'user' | ユーザーロール（user/admin） |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- email (UNIQUE)

### 2. user_profiles（ユーザープロフィール）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | プロフィールID |
| user_id | UUID | FK(users), UNIQUE, NOT NULL | ユーザーID |
| bio | TEXT | | 自己紹介 |
| avatar_url | VARCHAR(500) | | アバター画像URL |
| skills | JSON | | スキルタグ配列 |
| interests | JSON | | 興味・関心タグ配列 |
| available_time | INTEGER | | 週あたり活動可能時間（分） |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- user_id (UNIQUE)

### 3. goals（目標）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | 目標ID |
| user_id | UUID | FK(users), NOT NULL | ユーザーID |
| title | VARCHAR(255) | NOT NULL | タイトル |
| description | TEXT | | 説明 |
| category | ENUM | NOT NULL | カテゴリ（relationship/activity/sensitivity） |
| status | ENUM | DEFAULT 'active' | ステータス（active/completed/archived） |
| progress | INTEGER | DEFAULT 0 | 進捗率（0-100） |
| due_date | TIMESTAMP | | 期限 |
| completed_at | TIMESTAMP | | 完了日時 |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- user_id
- status
- category

### 4. steps（ステップ）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | ステップID |
| goal_id | UUID | FK(goals), NOT NULL | 目標ID |
| order | INTEGER | NOT NULL | 順序 |
| title | VARCHAR(255) | NOT NULL | タイトル |
| description | TEXT | | 説明 |
| status | ENUM | DEFAULT 'pending' | ステータス（pending/in_progress/completed/skipped） |
| estimated_minutes | INTEGER | | 所要時間（分） |
| notes | TEXT | | メモ |
| due_date | TIMESTAMP | | 期限 |
| completed_at | TIMESTAMP | | 完了日時 |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- goal_id
- status

### 5. logs（内省ログ）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | ログID |
| user_id | UUID | FK(users), NOT NULL | ユーザーID |
| title | VARCHAR(255) | NOT NULL | タイトル |
| content | TEXT | NOT NULL | 本文（Markdown） |
| tags | JSON | | タグ配列 |
| visibility | ENUM | DEFAULT 'private' | 公開設定（private/public） |
| related_event_id | UUID | FK(events) | 関連イベントID |
| related_goal_id | UUID | FK(goals) | 関連目標ID |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- user_id
- visibility
- created_at

### 6. events（イベント）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | イベントID |
| owner_id | UUID | FK(users), NOT NULL | 主催者ID |
| title | VARCHAR(255) | NOT NULL | タイトル |
| description | TEXT | | 説明 |
| start_date | TIMESTAMP | NOT NULL | 開始日時 |
| end_date | TIMESTAMP | | 終了日時 |
| location_type | ENUM | NOT NULL | 場所タイプ（online/offline/hybrid） |
| location_detail | VARCHAR(500) | | 場所詳細 |
| max_attendees | INTEGER | | 定員 |
| tags | JSON | | タグ配列 |
| status | ENUM | DEFAULT 'upcoming' | ステータス（upcoming/ongoing/completed/cancelled） |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- owner_id
- start_date
- status

### 7. event_participants（イベント参加者）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | 参加者ID |
| event_id | UUID | FK(events), NOT NULL | イベントID |
| user_id | UUID | FK(users), NOT NULL | ユーザーID |
| status | ENUM | DEFAULT 'joined' | ステータス（joined/cancelled） |
| joined_at | TIMESTAMP | NOT NULL | 参加日時 |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |

**インデックス**:
- event_id
- user_id
- UNIQUE(event_id, user_id)

### 8. projects（プロジェクト）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | プロジェクトID |
| owner_id | UUID | FK(users), NOT NULL | オーナーID |
| title | VARCHAR(255) | NOT NULL | タイトル |
| description | TEXT | | 説明 |
| category | ENUM | NOT NULL | カテゴリ（asobi/asoto） |
| status | ENUM | DEFAULT 'recruiting' | ステータス（recruiting/active/completed/archived） |
| start_date | TIMESTAMP | NOT NULL | 開始日 |
| end_date | TIMESTAMP | | 終了日 |
| frequency | VARCHAR(255) | | 活動頻度 |
| location_type | ENUM | NOT NULL | 場所タイプ（online/offline/hybrid） |
| location_detail | VARCHAR(500) | | 場所詳細 |
| is_recruiting | BOOLEAN | DEFAULT FALSE | 募集中フラグ |
| max_members | INTEGER | | 最大メンバー数 |
| required_skills | JSON | | 必要スキル配列 |
| tags | JSON | | タグ配列 |
| visibility | ENUM | DEFAULT 'public' | 公開設定（public/members_only） |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- owner_id
- status
- category
- is_recruiting

### 9. project_members（プロジェクトメンバー）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | メンバーID |
| project_id | UUID | FK(projects), NOT NULL | プロジェクトID |
| user_id | UUID | FK(users), NOT NULL | ユーザーID |
| role | ENUM | DEFAULT 'member' | ロール（owner/member） |
| status | ENUM | DEFAULT 'pending' | ステータス（pending/active/left） |
| contribution_role | VARCHAR(255) | | 担当役割 |
| contribution_points | INTEGER | DEFAULT 0 | 貢献度ポイント |
| joined_at | TIMESTAMP | | 参加日時 |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- project_id
- user_id
- UNIQUE(project_id, user_id)

### 10. project_tasks（プロジェクトタスク）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | タスクID |
| project_id | UUID | FK(projects), NOT NULL | プロジェクトID |
| assignee_id | UUID | FK(users) | 担当者ID |
| title | VARCHAR(255) | NOT NULL | タイトル |
| description | TEXT | | 説明 |
| status | ENUM | DEFAULT 'todo' | ステータス（todo/in_progress/done） |
| order | INTEGER | | 順序 |
| due_date | TIMESTAMP | | 期限 |
| completed_at | TIMESTAMP | | 完了日時 |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | 更新日時 |

**インデックス**:
- project_id
- assignee_id
- status

### 11. points（ポイント履歴）

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | ポイントID |
| user_id | UUID | FK(users), NOT NULL | ユーザーID |
| amount | INTEGER | NOT NULL | ポイント数 |
| action_type | VARCHAR(50) | NOT NULL | アクション種別 |
| reference_id | VARCHAR(255) | | 参照ID（目標ID、イベントIDなど） |
| description | TEXT | | 説明 |
| created_at | TIMESTAMP | NOT NULL | 作成日時 |

**インデックス**:
- user_id
- action_type
- created_at

## Enum定義

### UserRole
- `user` - 一般ユーザー
- `admin` - 管理者

### GoalCategory
- `relationship` - 関係性
- `activity` - 多動性
- `sensitivity` - 感受性

### GoalStatus
- `active` - 進行中
- `completed` - 完了
- `archived` - アーカイブ

### StepStatus
- `pending` - 未着手
- `in_progress` - 進行中
- `completed` - 完了
- `skipped` - スキップ

### LogVisibility
- `private` - 非公開
- `public` - 公開

### LocationType
- `online` - オンライン
- `offline` - オフライン
- `hybrid` - ハイブリッド

### EventStatus
- `upcoming` - 開催予定
- `ongoing` - 開催中
- `completed` - 完了
- `cancelled` - キャンセル

### ParticipantStatus
- `joined` - 参加
- `cancelled` - キャンセル

### ProjectCategory
- `asobi` - あそびプロジェクト
- `asoto` - あそとプロジェクト

### ProjectStatus
- `recruiting` - 募集中
- `active` - 進行中
- `completed` - 完了
- `archived` - アーカイブ

### MemberRole
- `owner` - オーナー
- `member` - メンバー

### MemberStatus
- `pending` - 参加リクエスト中
- `active` - 参加中
- `left` - 退出

### TaskStatus
- `todo` - 未着手
- `in_progress` - 進行中
- `done` - 完了

### ProjectVisibility
- `public` - 公開
- `members_only` - メンバーのみ

## データベース選択理由

### PostgreSQL
- JSON型のネイティブサポート（tags, skills, interests）
- UUID型のネイティブサポート
- トランザクションの堅牢性
- 拡張性（全文検索、GIS等）
- Supabase / Aurora Serverless での利用を想定

## マイグレーション戦略

1. 初期マイグレーションで全テーブルを作成
2. 外部キー制約を設定
3. インデックスを作成
4. Phase 2以降は追加マイグレーションで対応

## セキュリティ考慮事項

- パスワードは必ずハッシュ化（bcrypt）
- UUIDを主キーに使用（推測不可能）
- 削除は論理削除を推奨（将来的に`deleted_at`カラム追加）
- 個人情報を含むテーブルは暗号化を検討（将来）
