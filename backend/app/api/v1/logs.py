"""内省ログ（Log）API エンドポイント"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.log import Log, LogVisibility
from app.models.point import Point
from app.schemas.log import LogCreate, LogUpdate, LogResponse

router = APIRouter()


@router.post("/logs", response_model=LogResponse, status_code=status.HTTP_201_CREATED, tags=["内省ログ"])
async def create_log(
    log_data: LogCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    内省ログを作成

    - **title**: ログタイトル（必須）
    - **content**: 本文（必須、Markdown対応）
    - **tags**: タグ（配列）
    - **visibility**: 公開設定（public/private）
    - **related_event_id**: 関連イベントID
    - **related_goal_id**: 関連目標ID

    ログ作成で5ポイント付与されます。
    """
    log = Log(
        **log_data.model_dump(),
        user_id=current_user.id,
    )
    db.add(log)

    # ポイントを付与（5pt）
    point = Point(
        user_id=current_user.id,
        amount=5,
        action_type="log_create",
        reference_id=str(log.id),
        description=f"内省ログ「{log.title}」を投稿"
    )
    db.add(point)

    await db.commit()
    await db.refresh(log)
    return log


@router.get("/logs", response_model=List[LogResponse], tags=["内省ログ"])
async def get_logs(
    visibility: Optional[str] = Query(None, description="公開設定フィルタ（public/private）"),
    tag: Optional[str] = Query(None, description="タグフィルタ"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    内省ログ一覧を取得

    - 自分のログ（公開・非公開両方）
    - 他人の公開ログ

    クエリパラメータ:
    - **visibility**: public/private でフィルタ
    - **tag**: タグでフィルタ
    """
    # 基本クエリ: 自分のログ OR 公開ログ
    query = select(Log).where(
        or_(
            Log.user_id == current_user.id,
            Log.visibility == LogVisibility.PUBLIC
        )
    )

    # visibilityフィルタ
    if visibility:
        if visibility == "public":
            query = query.where(Log.visibility == LogVisibility.PUBLIC)
        elif visibility == "private":
            query = query.where(
                and_(
                    Log.user_id == current_user.id,
                    Log.visibility == LogVisibility.PRIVATE
                )
            )

    # タグフィルタ（PostgreSQLのJSON演算子を使用）
    if tag:
        # JSON配列に指定したタグが含まれているかチェック
        # JSONBの@>演算子を使用（contains）
        from sqlalchemy import cast, String
        from sqlalchemy.dialects.postgresql import JSONB
        query = query.where(cast(Log.tags, JSONB).op('@>')(cast([tag], JSONB)))

    query = query.order_by(Log.created_at.desc())

    result = await db.execute(query)
    logs = result.scalars().all()
    return logs


@router.get("/logs/{log_id}", response_model=LogResponse, tags=["内省ログ"])
async def get_log(
    log_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ログの詳細を取得

    自分のログまたは公開ログのみ取得可能
    """
    result = await db.execute(
        select(Log).where(
            Log.id == log_id,
            or_(
                Log.user_id == current_user.id,
                Log.visibility == LogVisibility.PUBLIC
            )
        )
    )
    log = result.scalar_one_or_none()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )

    return log


@router.patch("/logs/{log_id}", response_model=LogResponse, tags=["内省ログ"])
async def update_log(
    log_id: UUID,
    log_data: LogUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ログを更新

    自分のログのみ更新可能
    """
    result = await db.execute(
        select(Log).where(Log.id == log_id, Log.user_id == current_user.id)
    )
    log = result.scalar_one_or_none()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )

    # 更新
    update_data = log_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(log, field, value)

    await db.commit()
    await db.refresh(log)
    return log


@router.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["内省ログ"])
async def delete_log(
    log_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    ログを削除

    自分のログのみ削除可能
    """
    result = await db.execute(
        select(Log).where(Log.id == log_id, Log.user_id == current_user.id)
    )
    log = result.scalar_one_or_none()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )

    await db.delete(log)
    await db.commit()
    return None
