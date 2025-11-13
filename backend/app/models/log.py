from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class LogVisibility(str, enum.Enum):
    """ログ公開設定"""
    PRIVATE = "private"  # 非公開
    PUBLIC = "public"  # 公開


class Log(Base):
    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 基本情報
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  # Markdown
    tags = Column(JSON, default=list)  # ["読書会", "気づき"]
    visibility = Column(SQLEnum(LogVisibility), default=LogVisibility.PRIVATE)

    # 関連
    related_event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="SET NULL"))
    related_goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="SET NULL"))

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    user = relationship("User", back_populates="logs")
    related_event = relationship("Event", back_populates="logs")
    related_goal = relationship("Goal", back_populates="logs")
