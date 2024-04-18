from typing import List, Optional

from fastapi import APIRouter, Query

from models import ResponseData, PageData
from models.system.schemas import SysDictData
from services.system import dict_data_service

router = APIRouter()


@router.get("/list", tags=["dict_data"], response_model=ResponseData[List[SysDictData]])
async def list(
        dict_type: Optional[str] = Query(default=None, alias="dictType", title="字典类型"),
        dict_label: Optional[str] = Query(default=None, alias="dictLabel", title="字典标签"),
        dict_value: Optional[str] = Query(default=None, alias="dictValue", title="字典键值"),
):
    query = SysDictData(
        dict_type=dict_type,
        dict_label=dict_label,
        dict_value=dict_value
    )
    data = dict_data_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["dict_data"], response_model=ResponseData[PageData[SysDictData]])
async def page(
        page_index: int = Query(default=1, alias="pageIndex"),
        page_size: int = Query(default=10, alias="pageSize"),
        dict_type: Optional[str] = Query(default=None, alias="dictType", title="字典类型"),
        dict_label: Optional[str] = Query(default=None, alias="dictLabel", title="字典标签"),
        dict_value: Optional[str] = Query(default=None, alias="dictValue", title="字典键值"),
):
    query = SysDictData(
        dict_type=dict_type,
        dict_label=dict_label,
        dict_value=dict_value
    )
    data = dict_data_service.page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.get("/{id}", tags=["dict_data"], response_model=ResponseData[SysDictData])
async def get_info(id: int):
    return ResponseData.success(dict_data_service.get_by_id(id))


@router.post("", tags=['dict_data'], response_model=ResponseData[SysDictData])
async def create(config: SysDictData):
    return ResponseData.success(dict_data_service.create(config))


@router.put("", tags=['dict_data'], response_model=ResponseData[SysDictData])
async def update(config: SysDictData):
    return ResponseData.success(dict_data_service.update(config))


@router.delete("", tags=['dict_data'], response_model=ResponseData)
async def delete(id: str = Query(title="ID")):
    list = [int(f) for f in id.split(",")]
    dict_data_service.batch_delete(list)
    return ResponseData.success()
