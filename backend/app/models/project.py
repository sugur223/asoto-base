from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import LocationType
import uuid
import enum


class ProjectCategory(str, enum.Enum):
    """プロジェクトカテゴリ"""
    ASOBI = "asobi"  # あそびプロジェクト
    ASOTO = "asoto"  # あそとプロジェクト


class ProjectStatus(str, enum.Enum):
    """プロジェクトステータス"""
    RECRUITING = "recruiting"  # 募集中
    ACTIVE = "active"  # 進行中
    COMPLETED = "completed"  # 完了
    ARCHIVED = "archived"  # アーカイブ


class ProjectVisibility(str, enum.Enum):
    """プロジェクト公開設定"""
    PUBLIC = "public"  # 公開
    MEMBERS_ONLY = "members_only"  # メンバーのみ


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 基本情報
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(SQLEnum(ProjectCategory), nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.RECRUITING)

    # 期間・活動
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))
    frequency = Column(String(255))  # "週末月2回程度"

    # 場所
    location_type = Column(SQLEnum(LocationType), nullable=False)
    location_detail = Column(String(500))

    # メンバー募集
    is_recruiting = Column(Boolean, default=False)
    max_members = Column(Integer)
    required_skills = Column(JSON, default=list)  # ["農業知識", "写真撮影"]

    # メタ情報
    tags = Column(JSON, default=list)  # ["農業", "地域", "暮らし"]
    visibility = Column(SQLEnum(ProjectVisibility), default=ProjectVisibility.PUBLIC)

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    owner = relationship("User", back_populates="owned_projects")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
