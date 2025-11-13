from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class StepStatus(str, enum.Enum):
    """ステップステータス"""
    PENDING = "pending"  # 未着手
    IN_PROGRESS = "in_progress"  # 進行中
    COMPLETED = "completed"  # 完了
    SKIPPED = "skipped"  # スキップ


class Step(Base):
    __tablename__ = "steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)

    # 基本情報
    order = Column(Integer, nullable=False)  # 順序
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(StepStatus), default=StepStatus.PENDING)
    estimated_minutes = Column(Integer)  # 所要時間（分）
    notes = Column(Text)  # ユーザーのメモ

    # 日時
    due_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    goal = relationship("Goal", back_populates="steps")
