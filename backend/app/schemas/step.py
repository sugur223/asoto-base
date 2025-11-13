"""ステップ（Step）関連のスキーマ"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.step import StepStatus


class StepBase(BaseModel):
    """ステップベーススキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    order: int = Field(..., ge=0)
    estimated_minutes: Optional[int] = Field(None, ge=0)
    due_date: Optional[datetime] = None


class StepCreate(StepBase):
    """ステップ作成スキーマ"""
    pass


class StepUpdate(BaseModel):
    """ステップ更新スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)
    status: Optional[StepStatus] = None
    estimated_minutes: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None
    due_date: Optional[datetime] = None


class StepResponse(StepBase):
    """ステップレスポンススキーマ"""
    id: UUID
    goal_id: UUID
    status: StepStatus
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
