from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 非同期エンジン
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    future=True
)

# 非同期セッションメーカー
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def get_db():
    """データベースセッションの依存性注入"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
