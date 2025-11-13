import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash, create_access_token

# テスト用データベースURL（PostgreSQL）
# Docker Compose環境のPostgreSQLを使用
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/asotobase_test"


@pytest.fixture(scope="session")
def event_loop():
    """イベントループのフィクスチャ"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """テスト用データベースセッション"""
    # テスト用エンジン作成（PostgreSQL）
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False
    )

    # テーブル作成
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # セッション作成
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session

    # テーブル削除（クリーンアップ）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """テスト用HTTPクライアント"""

    # DBセッションをオーバーライド
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # オーバーライドをクリア
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db: AsyncSession) -> User:
    """テスト用ユーザー"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def test_user2(test_db: AsyncSession) -> User:
    """テスト用ユーザー2"""
    user = User(
        email="test2@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User 2",
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """認証ヘッダー"""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers2(test_user2: User) -> dict:
    """認証ヘッダー（ユーザー2）"""
    token = create_access_token(data={"sub": str(test_user2.id)})
    return {"Authorization": f"Bearer {token}"}
