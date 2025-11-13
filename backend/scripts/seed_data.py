"""サンプルデータ投入スクリプト

Phase 1のテストとデモ用のサンプルデータを作成します。

使い方:
    docker compose exec backend python scripts/seed_data.py
"""
import asyncio
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from uuid import uuid4

from app.core.config import settings
from app.core.security import get_password_hash
from app.models import (
    User, UserRole, UserProfile,
    Goal, GoalCategory, GoalStatus,
    Step, StepStatus,
    Log, LogVisibility,
    Event, EventStatus,
    EventParticipant, ParticipantStatus,
    Project, ProjectCategory, ProjectStatus, ProjectVisibility,
    ProjectMember, MemberRole, MemberStatus,
    ProjectTask, TaskStatus,
    Point,
    LocationType,
)


async def seed_data():
    """サンプルデータを投入"""
    # データベース接続
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("🌱 サンプルデータを投入開始...")

        # ユーザーを作成
        users = []
        user_data = [
            {
                "email": "alice@example.com",
                "full_name": "Alice",
                "password": "password123",
                "role": UserRole.USER,
                "bio": "自然が好きで、週末は農業体験に参加しています。",
                "skills": ["農業", "写真撮影", "ライティング"],
                "interests": ["食", "地域", "環境"],
                "available_time": 600,  # 10時間/週
            },
            {
                "email": "bob@example.com",
                "full_name": "Bob",
                "password": "password123",
                "role": UserRole.USER,
                "bio": "エンジニアですが、地域活動にも積極的に参加したいと思っています。",
                "skills": ["プログラミング", "デザイン", "企画"],
                "interests": ["テクノロジー", "コミュニティ", "教育"],
                "available_time": 300,  # 5時間/週
            },
            {
                "email": "carol@example.com",
                "full_name": "Carol",
                "password": "password123",
                "role": UserRole.ADMIN,
                "bio": "あそとbaseの運営をしています。みんなで楽しく活動しましょう！",
                "skills": ["コミュニティ運営", "ファシリテーション", "企画"],
                "interests": ["人", "つながり", "学び"],
                "available_time": 900,  # 15時間/週
            },
        ]

        print("👥 ユーザーを作成中...")
        for data in user_data:
            user = User(
                id=uuid4(),
                email=data["email"],
                hashed_password=get_password_hash(data["password"]),
                full_name=data["full_name"],
                role=data["role"],
                is_active=True,
            )
            session.add(user)
            await session.flush()

            # プロフィール作成
            profile = UserProfile(
                id=uuid4(),
                user_id=user.id,
                bio=data["bio"],
                skills=data["skills"],
                interests=data["interests"],
                available_time=data["available_time"],
            )
            session.add(profile)
            users.append(user)

        await session.commit()
        print(f"✅ {len(users)}人のユーザーを作成しました")

        # 目標とステップを作成
        print("🎯 目標とステップを作成中...")
        now = datetime.now()

        goal1 = Goal(
            id=uuid4(),
            user_id=users[0].id,
            title="月1回イベントに参加する",
            description="コミュニティとのつながりを深めるため、毎月1回はイベントに参加する",
            category=GoalCategory.RELATIONSHIP,
            status=GoalStatus.ACTIVE,
            progress=50,
            due_date=now + timedelta(days=90),
        )
        session.add(goal1)
        await session.flush()

        # ステップ追加
        steps = [
            Step(
                id=uuid4(),
                goal_id=goal1.id,
                order=1,
                title="興味のあるイベントを探す",
                description="イベント一覧から参加したいものを3つピックアップ",
                status=StepStatus.COMPLETED,
                estimated_minutes=30,
                completed_at=now - timedelta(days=5),
            ),
            Step(
                id=uuid4(),
                goal_id=goal1.id,
                order=2,
                title="1つ目のイベントに申し込む",
                description="来週の読書会に参加申込",
                status=StepStatus.COMPLETED,
                estimated_minutes=10,
                completed_at=now - timedelta(days=3),
            ),
            Step(
                id=uuid4(),
                goal_id=goal1.id,
                order=3,
                title="イベントに参加する",
                description="当日は15分前に到着して準備",
                status=StepStatus.IN_PROGRESS,
                estimated_minutes=120,
                due_date=now + timedelta(days=3),
            ),
        ]
        for step in steps:
            session.add(step)

        goal2 = Goal(
            id=uuid4(),
            user_id=users[1].id,
            title="プログラミング勉強会を企画する",
            description="初心者向けのプログラミング勉強会を開催し、知識を共有する",
            category=GoalCategory.ACTIVITY,
            status=GoalStatus.ACTIVE,
            progress=20,
            due_date=now + timedelta(days=60),
        )
        session.add(goal2)

        await session.commit()
        print("✅ 目標とステップを作成しました")

        # 内省ログを作成
        print("📝 内省ログを作成中...")
        logs = [
            Log(
                id=uuid4(),
                user_id=users[0].id,
                title="初めてのイベント参加",
                content="今日は初めて牧場見学イベントに参加しました。\n\n"
                        "実際に動物と触れ合えて、とても楽しかったです。"
                        "参加者の方々とも話せて、同じ興味を持つ人と繋がれたのが嬉しい。\n\n"
                        "次回は料理イベントにも参加してみようと思います。",
                tags=["イベント参加", "牧場見学", "振り返り"],
                visibility=LogVisibility.PUBLIC,
            ),
            Log(
                id=uuid4(),
                user_id=users[1].id,
                title="勉強会の企画について考える",
                content="プログラミング初心者向けの勉強会を企画したい。\n\n"
                        "内容:\n"
                        "- 基本的なHTML/CSS\n"
                        "- 簡単なWebページ作成\n"
                        "- 実践的なハンズオン形式\n\n"
                        "まずは会場を探すところから始めよう。",
                tags=["企画", "勉強会", "プログラミング"],
                visibility=LogVisibility.PRIVATE,
            ),
        ]
        for log in logs:
            session.add(log)

        await session.commit()
        print(f"✅ {len(logs)}件のログを作成しました")

        # イベントを作成
        print("🎉 イベントを作成中...")
        events = [
            Event(
                id=uuid4(),
                owner_id=users[2].id,
                title="週末農業体験",
                description="千葉の農園で野菜の収穫体験をします。初心者歓迎！\n\n"
                            "【内容】\n"
                            "- 季節の野菜の収穫\n"
                            "- 農業についてのミニ講座\n"
                            "- 収穫した野菜でランチ\n\n"
                            "【持ち物】\n動きやすい服装、帽子、タオル",
                start_date=now + timedelta(days=7),
                end_date=now + timedelta(days=7, hours=4),
                location_type=LocationType.OFFLINE,
                location_detail="千葉県○○市の農園（詳細は参加者にお知らせ）",
                max_attendees=15,
                tags=["農業", "体験", "食"],
                status=EventStatus.UPCOMING,
            ),
            Event(
                id=uuid4(),
                owner_id=users[1].id,
                title="オンライン読書会「哲学入門」",
                description="毎月恒例の読書会です。今月のテーマは「哲学入門」\n\n"
                            "課題図書: 『ソフィーの世界』\n"
                            "形式: 各自の感想をシェア + ディスカッション",
                start_date=now + timedelta(days=3),
                end_date=now + timedelta(days=3, hours=2),
                location_type=LocationType.ONLINE,
                location_detail="Zoom（リンクは前日に送付）",
                max_attendees=10,
                tags=["読書", "哲学", "オンライン"],
                status=EventStatus.UPCOMING,
            ),
        ]
        for event in events:
            session.add(event)

        await session.flush()

        # イベント参加者を追加
        participant = EventParticipant(
            id=uuid4(),
            event_id=events[0].id,
            user_id=users[0].id,
            status=ParticipantStatus.JOINED,
        )
        session.add(participant)

        await session.commit()
        print(f"✅ {len(events)}件のイベントを作成しました")

        # プロジェクトを作成
        print("🚀 プロジェクトを作成中...")
        project1 = Project(
            id=uuid4(),
            owner_id=users[2].id,
            title="新百姓プロジェクト",
            description="都市と農村をつなぐ新しい農業のかたち\n\n"
                        "週末や休日に農業体験をしながら、持続可能な暮らしについて学びます。"
                        "長期的には自分たちで野菜を育てて、地域とつながる活動を目指します。",
            category=ProjectCategory.ASOTO,
            status=ProjectStatus.ACTIVE,
            start_date=now,
            frequency="月2回程度",
            location_type=LocationType.OFFLINE,
            location_detail="千葉県○○市",
            is_recruiting=True,
            max_members=20,
            required_skills=["なし（初心者歓迎）"],
            tags=["農業", "地域", "持続可能性"],
            visibility=ProjectVisibility.PUBLIC,
        )
        session.add(project1)
        await session.flush()

        # プロジェクトメンバー
        members = [
            ProjectMember(
                id=uuid4(),
                project_id=project1.id,
                user_id=users[2].id,
                role=MemberRole.OWNER,
                status=MemberStatus.ACTIVE,
                contribution_role="プロジェクトリーダー",
                joined_at=now - timedelta(days=30),
            ),
            ProjectMember(
                id=uuid4(),
                project_id=project1.id,
                user_id=users[0].id,
                role=MemberRole.MEMBER,
                status=MemberStatus.ACTIVE,
                contribution_role="写真撮影・記録",
                joined_at=now - timedelta(days=20),
            ),
        ]
        for member in members:
            session.add(member)

        # プロジェクトタスク
        tasks = [
            ProjectTask(
                id=uuid4(),
                project_id=project1.id,
                assignee_id=users[2].id,
                title="次回の農業体験の日程調整",
                description="参加メンバーの都合を確認して日程を決める",
                status=TaskStatus.IN_PROGRESS,
                order=1,
                due_date=now + timedelta(days=7),
            ),
            ProjectTask(
                id=uuid4(),
                project_id=project1.id,
                assignee_id=users[0].id,
                title="前回のイベントレポート作成",
                description="写真をまとめてブログ記事を書く",
                status=TaskStatus.TODO,
                order=2,
                due_date=now + timedelta(days=10),
            ),
        ]
        for task in tasks:
            session.add(task)

        await session.commit()
        print("✅ プロジェクトを作成しました")

        # ポイントを作成
        print("⭐ ポイントを作成中...")
        points = [
            Point(
                id=uuid4(),
                user_id=users[0].id,
                amount=10,
                action_type="event_join",
                reference_id=str(events[0].id),
                description="イベント「週末農業体験」に参加",
            ),
            Point(
                id=uuid4(),
                user_id=users[0].id,
                amount=5,
                action_type="log_create",
                reference_id=str(logs[0].id),
                description="内省ログを投稿",
            ),
            Point(
                id=uuid4(),
                user_id=users[2].id,
                amount=50,
                action_type="project_create",
                reference_id=str(project1.id),
                description="あそとプロジェクト「新百姓プロジェクト」を作成",
            ),
        ]
        for point in points:
            session.add(point)

        await session.commit()
        print(f"✅ {len(points)}件のポイントを作成しました")

        print("\n🎉 サンプルデータの投入が完了しました！")
        print("\n📊 作成されたデータ:")
        print(f"  - ユーザー: {len(users)}人")
        print(f"  - 目標: 2件")
        print(f"  - ステップ: 3件")
        print(f"  - ログ: {len(logs)}件")
        print(f"  - イベント: {len(events)}件")
        print(f"  - プロジェクト: 1件")
        print(f"  - ポイント: {len(points)}件")
        print("\n🔑 テストユーザー:")
        print("  - alice@example.com / password123")
        print("  - bob@example.com / password123")
        print("  - carol@example.com / password123 (管理者)")


if __name__ == "__main__":
    asyncio.run(seed_data())
