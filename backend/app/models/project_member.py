from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class MemberRole(str, enum.Enum):
    """メンバーロール"""
    OWNER = "owner"  # オーナー
    MEMBER = "member"  # メンバー


class MemberStatus(str, enum.Enum):
    """メンバーステータス"""
    PENDING = "pending"  # 参加リクエスト中
    ACTIVE = "active"  # 参加中
    LEFT = "left"  # 退出


class ProjectMember(Base):
    __tablename__ = "project_members"
    __table_args__ = (
        UniqueConstraint('project_id', 'user_id', name='unique_project_user'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    role = Column(SQLEnum(MemberRole), default=MemberRole.MEMBER)
    status = Column(SQLEnum(MemberStatus), default=MemberStatus.PENDING)

    # メンバー情報
    contribution_role = Column(String(255))  # "写真担当", "ライティング"
    contribution_points = Column(Integer, default=0)  # このプロジェクトへの貢献度

    # 日時
    joined_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")
