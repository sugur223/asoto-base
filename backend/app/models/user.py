from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class UserRole(str, enum.Enum):
    """ユーザーロール"""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # リレーション
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")
    owned_events = relationship("Event", back_populates="owner", cascade="all, delete-orphan")
    event_participations = relationship("EventParticipant", back_populates="user", cascade="all, delete-orphan")
    owned_projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    project_memberships = relationship("ProjectMember", back_populates="user", cascade="all, delete-orphan")
    assigned_tasks = relationship("ProjectTask", back_populates="assignee")
    points = relationship("Point", back_populates="user", cascade="all, delete-orphan")
