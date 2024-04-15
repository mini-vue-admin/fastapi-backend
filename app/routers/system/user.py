from typing import List

from fastapi import APIRouter, Depends

from middlewares.oauth import get_current_active_user
from models import ResponseData
from models.system.schemas import User
from services.system.user import UserService

router = APIRouter()


@router.get("/users", tags=["users"], response_model=ResponseData[User])
async def read_users(user_service: UserService = Depends()):
    return ResponseData.success(
        user_service.get_by_id(1)
    )


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
