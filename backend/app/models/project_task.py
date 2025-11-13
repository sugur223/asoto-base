from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class TaskStatus(str, enum.Enum):
    """タスクステータス"""
    TODO = "todo"  # 未着手
    IN_PROGRESS = "in_progress"  # 進行中
    DONE = "done"  # 完了


class ProjectTask(Base):
    __tablename__ = "project_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))

    # 基本情報
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    order = Column(Integer)  # 順序

    # 日時
    due_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")
