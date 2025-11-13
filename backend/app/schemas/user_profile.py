"""ユーザープロフィール（UserProfile）関連のスキーマ"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class UserProfileBase(BaseModel):
    """ユーザープロフィールベーススキーマ"""
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    available_time: Optional[int] = Field(None, ge=0, description="週あたりの活動可能時間（分）")


class UserProfileUpdate(UserProfileBase):
    """ユーザープロフィール更新スキーマ"""
    pass


class UserProfileResponse(UserProfileBase):
    """ユーザープロフィールレスポンススキーマ"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
