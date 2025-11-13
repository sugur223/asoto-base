from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class GoalCategory(str, enum.Enum):
    """目標カテゴリ（あそと3要素）"""
    RELATIONSHIP = "relationship"  # 関係性
    ACTIVITY = "activity"  # 多動性
    SENSITIVITY = "sensitivity"  # 感受性


class GoalStatus(str, enum.Enum):
    """目標ステータス"""
    ACTIVE = "active"  # 進行中
    COMPLETED = "completed"  # 完了
    ARCHIVED = "archived"  # アーカイブ


class Goal(Base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 基本情報
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(SQLEnum(GoalCategory), nullable=False)
    status = Column(SQLEnum(GoalStatus), default=GoalStatus.ACTIVE)
    progress = Column(Integer, default=0)  # 0-100

    # 日時
    due_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    user = relationship("User", back_populates="goals")
    steps = relationship("Step", back_populates="goal", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="related_goal")
