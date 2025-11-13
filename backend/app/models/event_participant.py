from sqlalchemy import Column, DateTime, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class ParticipantStatus(str, enum.Enum):
    """参加者ステータス"""
    JOINED = "joined"  # 参加
    CANCELLED = "cancelled"  # キャンセル


class EventParticipant(Base):
    __tablename__ = "event_participants"
    __table_args__ = (
        UniqueConstraint('event_id', 'user_id', name='unique_event_user'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    status = Column(SQLEnum(ParticipantStatus), default=ParticipantStatus.JOINED)
    joined_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーション
    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="event_participations")
