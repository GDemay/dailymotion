from app.api.api_v1.endpoints import login, users
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"], prefix="/login")
api_router.include_router(users.router, tags=["user"], prefix="/user")
