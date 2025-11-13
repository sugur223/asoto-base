from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import LocationType
import uuid
import enum


class EventStatus(str, enum.Enum):
    """イベントステータス"""
    UPCOMING = "upcoming"  # 開催予定
    ONGOING = "ongoing"  # 開催中
    COMPLETED = "completed"  # 完了
    CANCELLED = "cancelled"  # キャンセル


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 基本情報
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))

    # 場所
    location_type = Column(SQLEnum(LocationType), nullable=False)
    location_detail = Column(String(500))

    # 定員
    max_attendees = Column(Integer)

    # メタ情報
    tags = Column(JSON, default=list)  # ["読書会", "オンライン"]
    status = Column(SQLEnum(EventStatus), default=EventStatus.UPCOMING)

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    owner = relationship("User", back_populates="owned_events")
    participants = relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="related_event")
