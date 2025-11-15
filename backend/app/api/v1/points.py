"""ポイント（Point）API エンドポイント"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.point import Point
from app.schemas.point import PointResponse, PointSummary

router = APIRouter()


@router.get("/users/me/points", response_model=PointSummary, tags=["ポイント"])
async def get_my_points(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    自分のポイント累計を取得

    **返却データ**:
    - **total_points**: 累計ポイント
    - **user_id**: ユーザーID
    """
    # ポイント累計を計算
    result = await db.execute(
        select(func.sum(Point.amount))
        .where(Point.user_id == current_user.id)
    )
    total_points = result.scalar() or 0

    return PointSummary(
        user_id=current_user.id,
        total_points=total_points
    )


@router.get("/users/me/points/history", response_model=List[PointResponse], tags=["ポイント"])
async def get_my_points_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    自分のポイント獲得履歴を取得

    新しい順に最大100件まで返します。

    **返却データ**:
    - **id**: ポイント記録ID
    - **user_id**: ユーザーID
    - **amount**: 獲得ポイント
    - **action_type**: アクションタイプ（step_complete, log_create など）
    - **reference_id**: 関連ID（目標ID、ログIDなど）
    - **description**: 説明
    - **created_at**: 獲得日時
    """
    result = await db.execute(
        select(Point)
        .where(Point.user_id == current_user.id)
        .order_by(desc(Point.created_at))
        .limit(100)
    )
    points = result.scalars().all()

    return points
