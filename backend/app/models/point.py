from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Point(Base):
    __tablename__ = "points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # ポイント情報
    amount = Column(Integer, nullable=False)  # ポイント数（負の値も可）
    action_type = Column(String(50), nullable=False)  # "goal_complete", "event_join", etc.
    reference_id = Column(String(255))  # 関連するIDは(目標ID、イベントIDなど)
    description = Column(Text)  # 説明

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーション
    user = relationship("User", back_populates="points")
