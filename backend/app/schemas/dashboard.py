"""ダッシュボード（Dashboard）スキーマ"""
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

from app.schemas.goal import GoalResponse
from app.schemas.log import LogResponse
from app.schemas.event import EventResponse


class PersonalAreaResponse(BaseModel):
    """個人エリアのレスポンス"""
    active_goals: List[GoalResponse]
    recent_logs: List[LogResponse]
    total_points: int
    model_config = ConfigDict(from_attributes=True)


class CommunityAreaResponse(BaseModel):
    """コミュニティエリアのレスポンス"""
    upcoming_events: List[EventResponse]
    recent_public_logs: List[LogResponse]
    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    """ダッシュボード全体のレスポンス"""
    personal: PersonalAreaResponse
    community: CommunityAreaResponse
    model_config = ConfigDict(from_attributes=True)
