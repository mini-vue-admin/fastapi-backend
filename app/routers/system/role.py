from typing import List, Optional

from fastapi import APIRouter, Query

from models import ResponseData, PageData
from models.system.schemas import SysRole, RoleMember, RoleMenu, SysMenu, SysUser
from services.system import role_service

router = APIRouter()


@router.get("/list", tags=["roles"], response_model=ResponseData[List[SysRole]])
async def list(
        role_key: Optional[str] = Query(default=None, alias="roleKey", title="角色键值"),
        role_name: Optional[str] = Query(default=None, alias="roleName", title="角色名称"),
):
    query = SysRole(
        role_key=role_key,
        role_name=role_name,
    )
    data = role_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["roles"], response_model=ResponseData[PageData[SysRole]])
async def page(
        page_index: int = Query(default=1, alias="pageIndex"),
        page_size: int = Query(default=10, alias="pageSize"),
        role_key: Optional[str] = Query(default=None, alias="roleKey", title="角色键值"),
        role_name: Optional[str] = Query(default=None, alias="roleName", title="角色名称"),
):
    query = SysRole(
        role_key=role_key,
        role_name=role_name,
    )
    data = role_service.page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.post("", tags=['roles'], response_model=ResponseData[SysRole])
async def create(dept: SysRole):
    return ResponseData.success(role_service.create(dept))


@router.put("", tags=['roles'], response_model=ResponseData[SysRole])
async def update(dept: SysRole):
    return ResponseData.success(role_service.update(dept))


@router.delete("", tags=['roles'], response_model=ResponseData)
async def delete(id: str = Query(title="ID")):
    list = [int(f) for f in id.split(",")]
    role_service.batch_delete(list)
    return ResponseData.success()


@router.get("/member", tags=['roles'], response_model=ResponseData[PageData[SysUser]])
async def member_page(
        page_index: int = Query(default=1, alias="pageIndex"),
        page_size: int = Query(default=10, alias="pageSize"),
        username: Optional[str] = Query(default=None, alias="username", title="用户名"),
        nickname: Optional[str] = Query(default=None, alias="nickname", title="用户昵称"),
        email: Optional[str] = Query(default=None, alias="email", title="邮箱"),
        phonenumber: Optional[str] = Query(default=None, alias="phonenumber", title="手机号"),
        status: Optional[str] = Query(default=None, alias="status", title="状态"),
        keyword: Optional[str] = Query(default=None, alias="params.keyWord", title="关键字",
                                       description="支持用户名，邮箱，昵称，手机号模糊查询"),
        role_id: Optional[int] = Query(default=None, alias="params.roleId", title="角色ID"),
        dis_role_id: Optional[int] = Query(default=None, alias="params.disRoleId", title="排除角色ID"),
):
    query = SysUser(
        username=username,
        nickname=nickname,
        email=email,
        phonenumber=phonenumber,
        status=status,
        params={
            'role_id': role_id,
            'dis_role_id': dis_role_id,
            'keyword': keyword
        }
    )
    data = role_service.member_page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.post("/member", tags=['roles'], response_model=ResponseData)
async def add_member(members: RoleMember):
    role_service.add_member(members)
    return ResponseData.success()


@router.delete("/member", tags=['roles'], response_model=ResponseData)
async def del_member(
        member_id: str = Query(alias="memberId", title="成员用户ID"),
        role_id: int = Query(alias="roleId", title="角色ID")
):
    id_list = [int(i) for i in member_id.split(",")]
    role_service.del_member(role_id, id_list)
    return ResponseData.success()


@router.get("/menu", tags=['roles'], response_model=ResponseData[List[SysMenu]])
async def list_menu(
        role_id: int = Query(alias="roleId", title="角色ID")
):
    return ResponseData.success(
        role_service.list_menu(role_id)
    )


@router.post("/menu", tags=['roles'], response_model=ResponseData)
async def add_menu(members: RoleMenu):
    role_service.add_menu(members)
    return ResponseData.success()


@router.get("/{id}", tags=["roles"], response_model=ResponseData[SysRole])
async def get_info(id: int):
    return ResponseData.success(role_service.get_by_id(id))
