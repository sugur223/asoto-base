"""ユーザープロフィール（UserProfile）API エンドポイント"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileUpdate, UserProfileResponse

router = APIRouter()


@router.get("/users/{user_id}/profile", response_model=UserProfileResponse, tags=["プロフィール"])
async def get_user_profile(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ユーザープロフィールを取得

    - **user_id**: ユーザーID

    誰でも他のユーザーのプロフィールを閲覧できます。
    """
    # ユーザープロフィールを取得
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile


@router.get("/users/me/profile", response_model=UserProfileResponse, tags=["プロフィール"])
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    自分のプロフィールを取得
    """
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile


@router.patch("/users/me/profile", response_model=UserProfileResponse, tags=["プロフィール"])
async def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    自分のプロフィールを更新

    - **bio**: 自己紹介
    - **avatar_url**: アバター画像URL
    - **skills**: スキルタグ（配列）
    - **interests**: 興味・関心タグ（配列）
    - **available_time**: 週あたりの活動可能時間（分）
    """
    # プロフィールを取得
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        # プロフィールが存在しない場合は作成
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    # 更新
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)
    return profile
