"""ポイント（Point）関連のスキーマ"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class PointBase(BaseModel):
    """ポイントベーススキーマ"""
    amount: int
    action_type: str = Field(..., max_length=50)
    reference_id: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class PointCreate(PointBase):
    """ポイント作成スキーマ"""
    user_id: UUID


class PointResponse(PointBase):
    """ポイントレスポンススキーマ"""
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PointSummary(BaseModel):
    """ポイント集計スキーマ"""
    user_id: UUID
    total_points: int
