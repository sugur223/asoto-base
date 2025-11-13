"""Pydantic Schemas"""
from app.schemas.user import UserBase, UserCreate, UserLogin, UserResponse, Token, TokenData
from app.schemas.user_profile import UserProfileBase, UserProfileUpdate, UserProfileResponse
from app.schemas.goal import GoalBase, GoalCreate, GoalUpdate, GoalResponse
from app.schemas.step import StepBase, StepCreate, StepUpdate, StepResponse
from app.schemas.log import LogBase, LogCreate, LogUpdate, LogResponse
from app.schemas.event import EventBase, EventCreate, EventUpdate, EventResponse
from app.schemas.project import (
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectTaskBase,
    ProjectTaskCreate,
    ProjectTaskUpdate,
    ProjectTaskResponse,
)
from app.schemas.point import PointBase, PointCreate, PointResponse, PointSummary
from app.schemas.dashboard import DashboardResponse, PersonalAreaResponse, CommunityAreaResponse

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
    # UserProfile
    "UserProfileBase",
    "UserProfileUpdate",
    "UserProfileResponse",
    # Goal
    "GoalBase",
    "GoalCreate",
    "GoalUpdate",
    "GoalResponse",
    # Step
    "StepBase",
    "StepCreate",
    "StepUpdate",
    "StepResponse",
    # Log
    "LogBase",
    "LogCreate",
    "LogUpdate",
    "LogResponse",
    # Event
    "EventBase",
    "EventCreate",
    "EventUpdate",
    "EventResponse",
    # Project
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectTaskBase",
    "ProjectTaskCreate",
    "ProjectTaskUpdate",
    "ProjectTaskResponse",
    # Point
    "PointBase",
    "PointCreate",
    "PointResponse",
    "PointSummary",
    # Dashboard
    "DashboardResponse",
    "PersonalAreaResponse",
    "CommunityAreaResponse",
]
