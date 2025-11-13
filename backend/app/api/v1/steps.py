"""ステップ（Step）API エンドポイント"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.goal import Goal
from app.models.step import Step, StepStatus
from app.models.point import Point
from app.schemas.step import StepCreate, StepUpdate, StepResponse

router = APIRouter()


@router.post("/goals/{goal_id}/steps", response_model=StepResponse, status_code=status.HTTP_201_CREATED, tags=["あそとステップ"])
async def create_step(
    goal_id: UUID,
    step_data: StepCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ステップを作成

    - **title**: ステップタイトル（必須）
    - **description**: 詳細説明
    - **order**: 順序（必須）
    - **estimated_minutes**: 予想所要時間（分）
    - **due_date**: 期限
    """
    # 目標の存在確認と権限チェック
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal = result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )

    step = Step(
        **step_data.model_dump(),
        goal_id=goal_id,
        status=StepStatus.PENDING
    )
    db.add(step)
    await db.commit()
    await db.refresh(step)
    return step


@router.patch("/steps/{step_id}", response_model=StepResponse, tags=["あそとステップ"])
async def update_step(
    step_id: UUID,
    step_data: StepUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ステップを更新
    """
    # ステップの取得と権限チェック
    result = await db.execute(
        select(Step)
        .join(Goal)
        .where(Step.id == step_id, Goal.user_id == current_user.id)
    )
    step = result.scalar_one_or_none()

    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step not found"
        )

    # 更新
    update_data = step_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(step, field, value)

    await db.commit()
    await db.refresh(step)
    return step


@router.post("/steps/{step_id}/complete", response_model=StepResponse, tags=["あそとステップ"])
async def complete_step(
    step_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ステップを完了

    ステップを完了状態にし、10ポイントを付与します。
    """
    # ステップの取得と権限チェック
    result = await db.execute(
        select(Step)
        .join(Goal)
        .where(Step.id == step_id, Goal.user_id == current_user.id)
    )
    step = result.scalar_one_or_none()

    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step not found"
        )

    # ステップを完了
    step.status = StepStatus.COMPLETED
    step.completed_at = datetime.now()

    # ポイントを付与（10pt）
    point = Point(
        user_id=current_user.id,
        amount=10,
        action_type="step_complete",
        reference_id=str(step_id),
        description=f"ステップ「{step.title}」を完了"
    )
    db.add(point)

    await db.commit()
    await db.refresh(step)
    return step


@router.delete("/steps/{step_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["あそとステップ"])
async def delete_step(
    step_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ステップを削除
    """
    # ステップの取得と権限チェック
    result = await db.execute(
        select(Step)
        .join(Goal)
        .where(Step.id == step_id, Goal.user_id == current_user.id)
    )
    step = result.scalar_one_or_none()

    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step not found"
        )

    await db.delete(step)
    await db.commit()
    return None
