""" This is the class use for routing the API. """
from fastapi import APIRouter

from app.api.endpoints import login, users

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"], prefix="/login")
api_router.include_router(users.router, tags=["user"], prefix="/user")
