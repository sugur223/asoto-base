"""目標（Goal）API エンドポイント"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.goal import Goal, GoalStatus
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

router = APIRouter()


@router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED, tags=["あそとステップ"])
async def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    目標を作成

    - **title**: 目標タイトル（必須）
    - **description**: 詳細説明
    - **category**: カテゴリ（relationship/activity/sensitivity）
    - **due_date**: 期限
    """
    goal = Goal(
        **goal_data.model_dump(),
        user_id=current_user.id,
        status=GoalStatus.ACTIVE,
        progress=0
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.get("/goals", response_model=List[GoalResponse], tags=["あそとステップ"])
async def get_goals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    自分の目標一覧を取得
    """
    result = await db.execute(
        select(Goal).where(Goal.user_id == current_user.id).order_by(Goal.created_at.desc())
    )
    goals = result.scalars().all()
    return goals


@router.get("/goals/{goal_id}", response_model=GoalResponse, tags=["あそとステップ"])
async def get_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    目標の詳細を取得
    """
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

    return goal


@router.patch("/goals/{goal_id}", response_model=GoalResponse, tags=["あそとステップ"])
async def update_goal(
    goal_id: UUID,
    goal_data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    目標を更新
    """
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

    # 更新
    update_data = goal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)

    await db.commit()
    await db.refresh(goal)
    return goal


@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["あそとステップ"])
async def delete_goal(
    goal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    目標を削除
    """
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

    await db.delete(goal)
    await db.commit()
    return None
