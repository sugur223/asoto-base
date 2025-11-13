from fastapi import APIRouter
from app.api.v1 import auth, goals, steps, logs, events, projects, dashboard, users, points

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["認証"])
api_router.include_router(dashboard.router)
api_router.include_router(users.router)
api_router.include_router(points.router)
api_router.include_router(goals.router)
api_router.include_router(steps.router)
api_router.include_router(logs.router)
api_router.include_router(events.router)
api_router.include_router(projects.router)
