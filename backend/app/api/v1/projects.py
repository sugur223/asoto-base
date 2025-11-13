"""プロジェクト（Project）API エンドポイント"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectCategory, ProjectStatus
from app.models.project_member import ProjectMember, MemberRole, MemberStatus
from app.models.project_task import ProjectTask, TaskStatus
from app.models.point import Point
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    ProjectTaskCreate, ProjectTaskUpdate, ProjectTaskResponse
)

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, tags=["プロジェクト"])
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    プロジェクトを作成

    - **title**: プロジェクトタイトル（必須）
    - **description**: 詳細説明
    - **category**: カテゴリ（asobi/asoto）
    - **start_date**: 開始日（必須）
    - **end_date**: 終了日
    - **frequency**: 活動頻度
    - **location_type**: 場所タイプ（online/offline/hybrid）
    - **location_detail**: 場所の詳細
    - **is_recruiting**: メンバー募集中
    - **max_members**: 最大メンバー数
    - **required_skills**: 必要なスキル
    - **tags**: タグ

    あそとプロジェクト作成で50pt、あそびプロジェクト作成で30pt付与されます。
    """
    project = Project(
        **project_data.model_dump(),
        owner_id=current_user.id,
        status=ProjectStatus.RECRUITING if project_data.is_recruiting else ProjectStatus.ACTIVE
    )
    db.add(project)
    await db.flush()

    # オーナーをメンバーとして登録
    owner_member = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role=MemberRole.OWNER,
        status=MemberStatus.ACTIVE,
        contribution_role="プロジェクトリーダー",
    )
    db.add(owner_member)

    # ポイントを付与（あそと: 50pt, あそび: 30pt）
    points = 50 if project_data.category == ProjectCategory.ASOTO else 30
    point = Point(
        user_id=current_user.id,
        amount=points,
        action_type="project_create",
        reference_id=str(project.id),
        description=f"プロジェクト「{project.title}」を作成"
    )
    db.add(point)

    await db.commit()
    await db.refresh(project)
    return project


@router.get("/projects", response_model=List[ProjectResponse], tags=["プロジェクト"])
async def get_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    プロジェクト一覧を取得

    公開プロジェクトを新しい順に表示
    """
    result = await db.execute(
        select(Project).order_by(Project.created_at.desc())
    )
    projects = result.scalars().all()
    return projects


@router.get("/projects/{project_id}", response_model=ProjectResponse, tags=["プロジェクト"])
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    プロジェクトの詳細を取得
    """
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project


@router.patch("/projects/{project_id}", response_model=ProjectResponse, tags=["プロジェクト"])
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    プロジェクトを更新

    プロジェクトオーナーのみ更新可能
    """
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # 更新
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["プロジェクト"])
async def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    プロジェクトを削除

    プロジェクトオーナーのみ削除可能
    """
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    await db.delete(project)
    await db.commit()
    return None


@router.post("/projects/{project_id}/join", tags=["プロジェクト"])
async def join_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    プロジェクトに参加リクエスト

    承認制のため、ステータスはPENDINGになります。
    承認後に10ポイント付与されます。
    """
    # プロジェクトの存在確認
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # 既に参加しているかチェック
    existing_result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id
        )
    )
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already member of this project"
        )

    # 参加リクエスト
    member = ProjectMember(
        project_id=project_id,
        user_id=current_user.id,
        role=MemberRole.MEMBER,
        status=MemberStatus.PENDING,
    )
    db.add(member)

    await db.commit()
    await db.refresh(member)

    return {"status": "pending", "project_id": str(project_id)}


@router.post("/projects/{project_id}/tasks", response_model=ProjectTaskResponse, status_code=status.HTTP_201_CREATED, tags=["プロジェクト"])
async def create_task(
    project_id: UUID,
    task_data: ProjectTaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    プロジェクトタスクを作成

    プロジェクトメンバーのみタスク作成可能
    """
    # プロジェクトメンバーかチェック
    member_result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
            ProjectMember.status == MemberStatus.ACTIVE
        )
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this project"
        )

    task = ProjectTask(
        **task_data.model_dump(),
        project_id=project_id,
        status=TaskStatus.TODO
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.patch("/projects/{project_id}/tasks/{task_id}", response_model=ProjectTaskResponse, tags=["プロジェクト"])
async def update_task(
    project_id: UUID,
    task_id: UUID,
    task_data: ProjectTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    タスクを更新

    プロジェクトメンバーのみ更新可能
    """
    # プロジェクトメンバーかチェック
    member_result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
            ProjectMember.status == MemberStatus.ACTIVE
        )
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this project"
        )

    # タスク取得
    task_result = await db.execute(
        select(ProjectTask).where(
            ProjectTask.id == task_id,
            ProjectTask.project_id == project_id
        )
    )
    task = task_result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # 更新
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/projects/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["プロジェクト"])
async def delete_task(
    project_id: UUID,
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    タスクを削除

    プロジェクトメンバーのみ削除可能
    """
    # プロジェクトメンバーかチェック
    member_result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
            ProjectMember.status == MemberStatus.ACTIVE
        )
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this project"
        )

    # タスク取得
    task_result = await db.execute(
        select(ProjectTask).where(
            ProjectTask.id == task_id,
            ProjectTask.project_id == project_id
        )
    )
    task = task_result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()
    return None
