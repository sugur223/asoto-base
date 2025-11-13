"""イベント（Event）関連のスキーマ"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.enums import LocationType
from app.models.event import EventStatus


class EventBase(BaseModel):
    """イベントベーススキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    location_type: LocationType
    location_detail: Optional[str] = Field(None, max_length=500)
    max_attendees: Optional[int] = Field(None, gt=0)
    tags: List[str] = Field(default_factory=list)


class EventCreate(EventBase):
    """イベント作成スキーマ"""
    pass


class EventUpdate(BaseModel):
    """イベント更新スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location_type: Optional[LocationType] = None
    location_detail: Optional[str] = Field(None, max_length=500)
    max_attendees: Optional[int] = Field(None, gt=0)
    tags: Optional[List[str]] = None
    status: Optional[EventStatus] = None


class EventResponse(EventBase):
    """イベントレスポンススキーマ"""
    id: UUID
    owner_id: UUID
    status: EventStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
