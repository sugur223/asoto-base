"""ダッシュボード（Dashboard）API エンドポイント"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.goal import Goal, GoalStatus
from app.models.log import Log, LogVisibility
from app.models.event import Event
from app.models.point import Point
from app.schemas.dashboard import DashboardResponse, PersonalAreaResponse, CommunityAreaResponse

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse, tags=["ダッシュボード"])
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ダッシュボードデータを取得

    **個人エリア**:
    - 進行中の目標（最大3件）
    - 最近のログ（最大3件）
    - 獲得ポイント（累計）

    **コミュニティエリア**:
    - 今後のイベント（最大5件）
    - 最近の公開ログ（最大5件）
    """
    # === 個人エリア ===

    # 進行中の目標（最大3件）
    active_goals_result = await db.execute(
        select(Goal)
        .where(
            Goal.user_id == current_user.id,
            Goal.status == GoalStatus.ACTIVE
        )
        .order_by(Goal.created_at.desc())
        .limit(3)
    )
    active_goals = active_goals_result.scalars().all()

    # 最近のログ（最大3件）
    recent_logs_result = await db.execute(
        select(Log)
        .where(Log.user_id == current_user.id)
        .order_by(Log.created_at.desc())
        .limit(3)
    )
    recent_logs = recent_logs_result.scalars().all()

    # 獲得ポイント（累計）
    total_points_result = await db.execute(
        select(func.sum(Point.amount))
        .where(Point.user_id == current_user.id)
    )
    total_points = total_points_result.scalar() or 0

    # === コミュニティエリア ===

    # 今後のイベント（最大5件、開始日時が現在より未来のもの）
    upcoming_events_result = await db.execute(
        select(Event)
        .where(Event.start_date >= datetime.now())
        .order_by(Event.start_date.asc())
        .limit(5)
    )
    upcoming_events = upcoming_events_result.scalars().all()

    # 最近の公開ログ（最大5件）
    recent_public_logs_result = await db.execute(
        select(Log)
        .where(Log.visibility == LogVisibility.PUBLIC)
        .order_by(Log.created_at.desc())
        .limit(5)
    )
    recent_public_logs = recent_public_logs_result.scalars().all()

    # レスポンス構築
    personal_area = PersonalAreaResponse(
        active_goals=active_goals,
        recent_logs=recent_logs,
        total_points=total_points
    )

    community_area = CommunityAreaResponse(
        upcoming_events=upcoming_events,
        recent_public_logs=recent_public_logs
    )

    return DashboardResponse(
        personal=personal_area,
        community=community_area
    )
