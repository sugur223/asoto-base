from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """ユーザーベーススキーマ"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """ユーザー作成スキーマ"""
    password: str


class UserLogin(BaseModel):
    """ログインスキーマ"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """ユーザーレスポンススキーマ"""
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """トークンレスポンス"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """トークンデータ"""
    user_id: Optional[str] = None
