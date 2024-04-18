from typing import List, Optional

from fastapi import APIRouter, Query

from models import ResponseData, PageData
from models.system.schemas import SysDept, DeptMember
from services.system import dept_service

router = APIRouter()


@router.get("/list", tags=["depts"], response_model=ResponseData[List[SysDept]])
async def list(
        parent_id: Optional[str] = Query(default=None, alias="parentId", title="父部门ID"),
        dept_name: Optional[str] = Query(default=None, alias="deptName", title="部门名称"),
):
    query = SysDept(
        parent_id=parent_id,
        dept_name=dept_name,
    )
    data = dept_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["depts"], response_model=ResponseData[PageData[SysDept]])
async def page(
        page_index: int = Query(default=1, alias="pageIndex"),
        page_size: int = Query(default=10, alias="pageSize"),
        parent_id: Optional[str] = Query(default=None, alias="parentId", title="父部门ID"),
        dept_name: Optional[str] = Query(default=None, alias="deptName", title="部门名称"),
):
    query = SysDept(
        parent_id=parent_id,
        dept_name=dept_name,
    )
    data = dept_service.page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.get("/tree", tags=["depts"], response_model=ResponseData[List[SysDept]])
async def tree(
        parent_id: Optional[str] = Query(default=None, alias="parentId", title="父部门ID"),
        dept_name: Optional[str] = Query(default=None, alias="deptName", title="部门名称"),
):
    query = SysDept(
        parent_id=parent_id,
        dept_name=dept_name,
    )
    data = dept_service.tree(query)
    return ResponseData.success(data)


@router.get("/{id}", tags=["depts"], response_model=ResponseData[SysDept])
async def get_info(id: int):
    return ResponseData.success(dept_service.get_by_id(id))


@router.post("", tags=['depts'], response_model=ResponseData[SysDept])
async def create(dept: SysDept):
    return ResponseData.success(dept_service.create(dept))


@router.put("", tags=['depts'], response_model=ResponseData[SysDept])
async def update(dept: SysDept):
    return ResponseData.success(dept_service.update(dept))


@router.delete("", tags=['depts'], response_model=ResponseData)
async def delete(id: str = Query(title="ID")):
    list = [int(f) for f in id.split(",")]
    dept_service.batch_delete(list)
    return ResponseData.success()


@router.post("/member", tags=['depts'], response_model=ResponseData)
async def add_member(members: DeptMember):
    dept_service.add_member(members)
    return ResponseData.success()


@router.delete("/member", tags=['depts'], response_model=ResponseData)
async def del_member(
        member_id: str = Query(alias="memberId", title="成员用户ID"),
        dept_id: int = Query(alias="deptId", title="部门ID")
):
    id_list = [int(i) for i in member_id.split(",")]
    dept_service.del_member(dept_id, id_list)
    return ResponseData.success()
