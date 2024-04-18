from typing import List, Optional

from fastapi import APIRouter, Query

from models import ResponseData, PageData
from models.system.schemas import SysDictType
from services.system import dict_type_service

router = APIRouter()


@router.get("/list", tags=["dict_type"], response_model=ResponseData[List[SysDictType]])
async def list(
        dict_type: Optional[str] = Query(default=None, alias="dictType", title="字典类型"),
        dict_name: Optional[str] = Query(default=None, alias="dictName", title="字典名称"),
):
    query = SysDictType(
        dict_name=dict_name,
        dict_type=dict_type
    )
    data = dict_type_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["dict_type"], response_model=ResponseData[PageData[SysDictType]])
async def page(
        page_index: int = Query(default=1, alias="pageIndex"),
        page_size: int = Query(default=10, alias="pageSize"),
        dict_type: Optional[str] = Query(default=None, alias="dictType", title="字典类型"),
        dict_name: Optional[str] = Query(default=None, alias="dictName", title="字典名称"),
):
    query = SysDictType(
        dict_name=dict_name,
        dict_type=dict_type,
    )
    data = dict_type_service.page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.get("/{id}", tags=["dict_type"], response_model=ResponseData[SysDictType])
async def get_info(id: int):
    return ResponseData.success(dict_type_service.get_by_id(id))


@router.post("", tags=['dict_type'], response_model=ResponseData[SysDictType])
async def create(config: SysDictType):
    return ResponseData.success(dict_type_service.create(config))


@router.put("", tags=['dict_type'], response_model=ResponseData[SysDictType])
async def update(config: SysDictType):
    return ResponseData.success(dict_type_service.update(config))


@router.delete("", tags=['dict_type'], response_model=ResponseData)
async def delete(id: str = Query(title="ID")):
    list = [int(f) for f in id.split(",")]
    dict_type_service.batch_delete(list)
    return ResponseData.success()
