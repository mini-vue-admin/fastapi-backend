from typing import List

from fastapi import APIRouter, Query

from models import ResponseData, PageData
from models.system.schemas import SysConfig
from services.system import config_service

router = APIRouter()


@router.get("/list", tags=["configs"], response_model=ResponseData[List[SysConfig]])
async def list():
    query = SysConfig()
    data = config_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["configs"], response_model=ResponseData[PageData[SysConfig]])
async def page(
        page_num: int = Query(default=1, alias="pageNum"),
        page_size: int = Query(default=10, alias="pageSize"),
):
    query = SysConfig()
    data = config_service.page(query, PageData(page_num=page_num, page_size=page_size))
    return ResponseData.success(data)


@router.get("/{id}", tags=["configs"], response_model=ResponseData[SysConfig])
async def get_info(id: int):
    return ResponseData.success(config_service.get_by_id(id))


@router.post("", tags=['configs'], response_model=ResponseData[SysConfig])
async def create(config: SysConfig):
    return ResponseData.success(config_service.create(config))


@router.put("", tags=['configs'], response_model=ResponseData[SysConfig])
async def create(config: SysConfig):
    return ResponseData.success(config_service.update(config))


@router.delete("/{id}", tags=['configs'], response_model=ResponseData)
async def create(id: str):
    list = [int(f) for f in id.split(",")]
    config_service.batch_delete(list)
    return ResponseData.success()
