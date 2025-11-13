"""プロジェクト（Project）関連のスキーマ"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.enums import LocationType
from app.models.project import ProjectCategory, ProjectStatus, ProjectVisibility


class ProjectBase(BaseModel):
    """プロジェクトベーススキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: ProjectCategory
    start_date: datetime
    end_date: Optional[datetime] = None
    frequency: Optional[str] = Field(None, max_length=255)
    location_type: LocationType
    location_detail: Optional[str] = Field(None, max_length=500)
    is_recruiting: bool = False
    max_members: Optional[int] = Field(None, gt=0)
    required_skills: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    visibility: ProjectVisibility = ProjectVisibility.PUBLIC


class ProjectCreate(ProjectBase):
    """プロジェクト作成スキーマ"""
    pass


class ProjectUpdate(BaseModel):
    """プロジェクト更新スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[ProjectCategory] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    frequency: Optional[str] = Field(None, max_length=255)
    location_type: Optional[LocationType] = None
    location_detail: Optional[str] = Field(None, max_length=500)
    is_recruiting: Optional[bool] = None
    max_members: Optional[int] = Field(None, gt=0)
    required_skills: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    visibility: Optional[ProjectVisibility] = None


class ProjectResponse(ProjectBase):
    """プロジェクトレスポンススキーマ"""
    id: UUID
    owner_id: UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectTaskBase(BaseModel):
    """プロジェクトタスクベーススキーマ"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    assignee_id: Optional[UUID] = None
    order: Optional[int] = Field(None, ge=0)
    due_date: Optional[datetime] = None


class ProjectTaskCreate(ProjectTaskBase):
    """プロジェクトタスク作成スキーマ"""
    pass


class ProjectTaskUpdate(BaseModel):
    """プロジェクトタスク更新スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    assignee_id: Optional[UUID] = None
    status: Optional[str] = None  # TaskStatus enum
    order: Optional[int] = Field(None, ge=0)
    due_date: Optional[datetime] = None


class ProjectTaskResponse(ProjectTaskBase):
    """プロジェクトタスクレスポンススキーマ"""
    id: UUID
    project_id: UUID
    status: str  # TaskStatus enum
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
