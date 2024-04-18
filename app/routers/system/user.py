from fastapi import APIRouter, Depends, Query

from middlewares.oauth import get_current_active_user
from models import ResponseData, PageData
from models.system.schemas import SysUser
from services.system import user_service

router = APIRouter()


@router.get("/page", tags=["users"], response_model=ResponseData[PageData[SysUser]])
async def page(page_num: int = Query(default=1, alias="pageNum"),
               page_size: int = Query(default=10, alias="pageSize"), ):
    user = SysUser(
        dept_id=12
    )

    data = user_service.page(user, PageData(page_num=page_num, page_size=page_size))
    return ResponseData.success(data)


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.get("/users/me")
async def read_users_me(current_user: SysUser = Depends(get_current_active_user)):
    return current_user
