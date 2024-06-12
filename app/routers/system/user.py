from typing import Optional, List

from fastapi import APIRouter, Query, Depends

from middlewares.oauth import get_current_active_user, PrincipleUser
from models import ResponseData, PageData
from models.system.schemas import SysUser
from services.system import user_service

router = APIRouter()


@router.get("/list", tags=["users"], response_model=ResponseData[List[SysUser]])
async def list(
        dept_id: Optional[int] = Query(default=None, alias="deptId", title="部门ID"),
        username: Optional[str] = Query(default=None, alias="username", title="用户名"),
        nickname: Optional[str] = Query(default=None, alias="nickname", title="用户昵称"),
        email: Optional[str] = Query(default=None, alias="email", title="邮箱"),
        phonenumber: Optional[str] = Query(default=None, alias="phonenumber", title="手机号"),
        status: Optional[str] = Query(default=None, alias="status", title="状态"),
        keyword: Optional[str] = Query(default=None, alias="params.keyWord", title="关键字"),
        dis_dept_id: Optional[int] = Query(default=None, alias="params.disDeptId", title="排除部门ID")
):
    query = SysUser(
        dept_id=dept_id,
        username=username,
        nickname=nickname,
        email=email,
        phonenumber=phonenumber,
        status=status,
        params={
            'keyword': keyword,
            'dis_dept_id': dis_dept_id
        }
    )
    data = user_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["users"], response_model=ResponseData[PageData[SysUser]])
async def page(page_index: int = Query(default=1, alias="pageIndex"),
               page_size: int = Query(default=10, alias="pageSize"),
               dept_id: Optional[int] = Query(default=None, alias="deptId", title="部门ID"),
               username: Optional[str] = Query(default=None, alias="username", title="用户名"),
               nickname: Optional[str] = Query(default=None, alias="nickname", title="用户昵称"),
               email: Optional[str] = Query(default=None, alias="email", title="邮箱"),
               phonenumber: Optional[str] = Query(default=None, alias="phonenumber", title="手机号"),
               status: Optional[str] = Query(default=None, alias="status", title="状态"),
               keyword: Optional[str] = Query(default=None, alias="params.keyWord", title="关键字"),
               dis_dept_id: Optional[int] = Query(default=None, alias="params.disDeptId", title="排除部门ID")
               ):
    query = SysUser(
        dept_id=dept_id,
        username=username,
        nickname=nickname,
        email=email,
        phonenumber=phonenumber,
        status=status,
        params={
            'keyword': keyword,
            'dis_dept_id': dis_dept_id
        }
    )

    data = user_service.page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.get("/own", tags=["users"], response_model=ResponseData[PrincipleUser])
async def get_self(principle: PrincipleUser = Depends(get_current_active_user)):
    return ResponseData.success(principle)


@router.get("/{id}", tags=["users"], response_model=ResponseData[SysUser])
async def get_info(id: int):
    return ResponseData.success(user_service.get_by_id(id))


@router.post("/{id}/resetPassword", tags=["users"], response_model=ResponseData)
async def reset_pwd(id: int):
    user_service.reset_pwd(id)
    return ResponseData.success()


@router.post("", tags=['users'], response_model=ResponseData[SysUser])
async def create(user: SysUser):
    return ResponseData.success(user_service.create(user))


@router.put("", tags=['users'], response_model=ResponseData[SysUser])
async def update(user: SysUser):
    return ResponseData.success(user_service.update(user))


@router.delete("", tags=['users'], response_model=ResponseData)
async def delete(id: str = Query(title="ID")):
    list = [int(f) for f in id.split(",")]
    user_service.batch_delete(list)
    return ResponseData.success()
