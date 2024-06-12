from typing import List, Optional

from fastapi import APIRouter, Query, Depends

from middlewares.oauth import get_current_active_user, PrincipleUser
from models import ResponseData, PageData
from models.system.schemas import SysMenu
from services.system import menu_service

router = APIRouter()


@router.get("/list", tags=["menus"], response_model=ResponseData[List[SysMenu]])
async def list(
        parent_id: Optional[int] = Query(default=None, alias="parentId", title="父节点ID"),
        menu_title: Optional[str] = Query(default=None, alias="menuTitle", title="菜单标题"),
        menu_type: Optional[str] = Query(default=None, alias="menuType", title="菜单类型"),
        menu_name: Optional[str] = Query(default=None, alias="menuName", title="菜单名称"),
        path: Optional[str] = Query(default=None, title="菜单路径"),
        component: Optional[str] = Query(default=None, title="组件名称"),
        status: Optional[str] = Query(default=None, title="状态"),
):
    query = SysMenu(
        parent_id=parent_id,
        menu_title=menu_title,
        menu_name=menu_name,
        menu_type=menu_type,
        path=path,
        component=component,
        status=status,
    )
    data = menu_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["menus"], response_model=ResponseData[PageData[SysMenu]])
async def page(page_index: int = Query(default=1, alias="pageIndex"),
               page_size: int = Query(default=10, alias="pageSize"),
               parent_id: Optional[int] = Query(default=None, alias="parentId", title="父节点ID"),
               menu_title: Optional[str] = Query(default=None, alias="menuTitle", title="菜单标题"),
               menu_type: Optional[str] = Query(default=None, alias="menuType", title="菜单类型"),
               menu_name: Optional[str] = Query(default=None, alias="menuName", title="菜单名称"),
               path: Optional[str] = Query(default=None, title="菜单路径"),
               component: Optional[str] = Query(default=None, title="组件名称"),
               status: Optional[str] = Query(default=None, title="状态"),
               ):
    query = SysMenu(
        parent_id=parent_id,
        menu_title=menu_title,
        menu_name=menu_name,
        menu_type=menu_type,
        path=path,
        component=component,
        status=status,
    )
    data = menu_service.page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.get("/tree", tags=["menus"], response_model=ResponseData[List[SysMenu]])
async def tree(
        parent_id: Optional[int] = Query(default=None, alias="parentId", title="父节点ID"),
        menu_title: Optional[str] = Query(default=None, alias="menuTitle", title="菜单标题"),
        menu_type: Optional[str] = Query(default=None, alias="menuType", title="菜单类型"),
        menu_name: Optional[str] = Query(default=None, alias="menuName", title="菜单名称"),
        path: Optional[str] = Query(default=None, title="菜单路径"),
        component: Optional[str] = Query(default=None, title="组件名称"),
        status: Optional[str] = Query(default=None, title="状态"),
        principle: PrincipleUser = Depends(get_current_active_user),
):
    query = SysMenu(
        parent_id=parent_id,
        menu_title=menu_title,
        menu_name=menu_name,
        menu_type=menu_type,
        path=path,
        component=component,
        status=status,
    )
    data = menu_service.tree(query, principle)
    return ResponseData.success(data)


@router.get("/{id}", tags=["menus"], response_model=ResponseData[SysMenu])
async def get_info(id: int):
    return ResponseData.success(menu_service.get_by_id(id))


@router.post("", tags=['menus'], response_model=ResponseData[SysMenu])
async def create(menu: SysMenu):
    return ResponseData.success(menu_service.create(menu))


@router.put("", tags=['menus'], response_model=ResponseData[SysMenu])
async def update(config: SysMenu):
    return ResponseData.success(menu_service.update(config))


@router.delete("", tags=['menus'], response_model=ResponseData)
async def delete(id: str = Query(title="ID")):
    list = [int(f) for f in id.split(",")]
    menu_service.batch_delete(list)
    return ResponseData.success()
