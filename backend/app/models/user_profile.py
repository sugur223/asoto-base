from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # プロフィール情報
    bio = Column(Text)
    avatar_url = Column(String(500))
    skills = Column(JSON, default=list)  # ["Python", "React", "デザイン"]
    interests = Column(JSON, default=list)  # ["農業", "AI", "地域活性化"]
    available_time = Column(Integer)  # 週あたり活動可能時間（分）

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    user = relationship("User", back_populates="profile")
