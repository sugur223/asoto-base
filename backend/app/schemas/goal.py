"""目標（Goal）関連のスキーマ"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.goal import GoalCategory, GoalStatus


class GoalBase(BaseModel):
    """目標ベーススキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: GoalCategory
    due_date: Optional[datetime] = None


class GoalCreate(GoalBase):
    """目標作成スキーマ"""
    pass


class GoalUpdate(BaseModel):
    """目標更新スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[GoalCategory] = None
    status: Optional[GoalStatus] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    due_date: Optional[datetime] = None


class GoalResponse(GoalBase):
    """目標レスポンススキーマ"""
    id: UUID
    user_id: UUID
    status: GoalStatus
    progress: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
