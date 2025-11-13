"""内省ログ（Log）関連のスキーマ"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.log import LogVisibility


class LogBase(BaseModel):
    """ログベーススキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    tags: List[str] = Field(default_factory=list)
    visibility: LogVisibility = LogVisibility.PRIVATE
    related_event_id: Optional[UUID] = None
    related_goal_id: Optional[UUID] = None


class LogCreate(LogBase):
    """ログ作成スキーマ"""
    pass


class LogUpdate(BaseModel):
    """ログ更新スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[List[str]] = None
    visibility: Optional[LogVisibility] = None
    related_event_id: Optional[UUID] = None
    related_goal_id: Optional[UUID] = None


class LogResponse(LogBase):
    """ログレスポンススキーマ"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
