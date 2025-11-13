"""イベント（Event）API エンドポイント"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.event import Event, EventStatus
from app.models.event_participant import EventParticipant, ParticipantStatus
from app.models.point import Point
from app.schemas.event import EventCreate, EventUpdate, EventResponse

router = APIRouter()


@router.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED, tags=["イベント"])
async def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベントを作成

    - **title**: イベントタイトル（必須）
    - **description**: 詳細説明
    - **start_date**: 開始日時（必須）
    - **end_date**: 終了日時
    - **location_type**: 場所タイプ（online/offline/hybrid）
    - **location_detail**: 場所の詳細
    - **max_attendees**: 定員
    - **tags**: タグ

    イベント作成で50ポイント付与されます。
    """
    event = Event(
        **event_data.model_dump(),
        owner_id=current_user.id,
        status=EventStatus.UPCOMING
    )
    db.add(event)

    # ポイントを付与（50pt）
    point = Point(
        user_id=current_user.id,
        amount=50,
        action_type="event_create",
        reference_id=str(event.id),
        description=f"イベント「{event.title}」を作成"
    )
    db.add(point)

    await db.commit()
    await db.refresh(event)
    return event


@router.get("/events", response_model=List[EventResponse], tags=["イベント"])
async def get_events(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベント一覧を取得

    今後のイベントを新しい順に表示
    """
    result = await db.execute(
        select(Event).order_by(Event.start_date.desc())
    )
    events = result.scalars().all()
    return events


@router.get("/events/{event_id}", response_model=EventResponse, tags=["イベント"])
async def get_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベントの詳細を取得
    """
    result = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event


@router.patch("/events/{event_id}", response_model=EventResponse, tags=["イベント"])
async def update_event(
    event_id: UUID,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベントを更新

    イベント作成者のみ更新可能
    """
    result = await db.execute(
        select(Event).where(Event.id == event_id, Event.owner_id == current_user.id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # 更新
    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)

    await db.commit()
    await db.refresh(event)
    return event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["イベント"])
async def delete_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベントを削除

    イベント作成者のみ削除可能
    """
    result = await db.execute(
        select(Event).where(Event.id == event_id, Event.owner_id == current_user.id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    await db.delete(event)
    await db.commit()
    return None


@router.post("/events/{event_id}/join", tags=["イベント"])
async def join_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベントに参加

    イベント参加で10ポイント付与されます。
    """
    # イベントの存在確認
    result = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # 既に参加しているかチェック
    existing_result = await db.execute(
        select(EventParticipant).where(
            EventParticipant.event_id == event_id,
            EventParticipant.user_id == current_user.id,
            EventParticipant.status == ParticipantStatus.JOINED
        )
    )
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already joined this event"
        )

    # 参加登録
    participant = EventParticipant(
        event_id=event_id,
        user_id=current_user.id,
        status=ParticipantStatus.JOINED
    )
    db.add(participant)

    # ポイントを付与（10pt）
    point = Point(
        user_id=current_user.id,
        amount=10,
        action_type="event_join",
        reference_id=str(event_id),
        description=f"イベント「{event.title}」に参加"
    )
    db.add(point)

    await db.commit()
    await db.refresh(participant)

    return {"status": "joined", "event_id": str(event_id)}


@router.delete("/events/{event_id}/leave", status_code=status.HTTP_204_NO_CONTENT, tags=["イベント"])
async def leave_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベントから離脱
    """
    # 参加記録を取得
    result = await db.execute(
        select(EventParticipant).where(
            EventParticipant.event_id == event_id,
            EventParticipant.user_id == current_user.id,
            EventParticipant.status == ParticipantStatus.JOINED
        )
    )
    participant = result.scalar_one_or_none()

    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participation not found"
        )

    # ステータスをキャンセルに変更
    participant.status = ParticipantStatus.CANCELLED

    await db.commit()
    return None


@router.get("/events/{event_id}/participants", tags=["イベント"])
async def get_participants(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    イベント参加者一覧を取得
    """
    # イベントの存在確認
    event_result = await db.execute(
        select(Event).where(Event.id == event_id)
    )
    event = event_result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # 参加者を取得
    result = await db.execute(
        select(EventParticipant)
        .where(
            EventParticipant.event_id == event_id,
            EventParticipant.status == ParticipantStatus.JOINED
        )
        .order_by(EventParticipant.joined_at.desc())
    )
    participants = result.scalars().all()

    return [
        {
            "id": str(p.id),
            "user_id": str(p.user_id),
            "status": p.status.value,
            "joined_at": p.joined_at.isoformat() if p.joined_at else None,
        }
        for p in participants
    ]
