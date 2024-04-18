from typing import List, Optional

from fastapi import APIRouter, Query

from models import ResponseData, PageData
from models.system.schemas import SysConfig
from services.system import config_service

router = APIRouter()


@router.get("/list", tags=["configs"], response_model=ResponseData[List[SysConfig]])
async def list(
        config_name: Optional[str] = Query(default=None, alias="configName", title="配置名称"),
        config_type: Optional[str] = Query(default=None, alias="configType", title="配置类型"),
        config_key: Optional[str] = Query(default=None, alias="configKey", title="配置键名"),
        config_value: Optional[str] = Query(default=None, alias="configValue", title="配置键值"),
):
    query = SysConfig(
        config_name=config_name,
        config_type=config_type,
        config_key=config_key,
        config_value=config_value,
    )
    data = config_service.list(query)
    return ResponseData.success(data)


@router.get("/page", tags=["configs"], response_model=ResponseData[PageData[SysConfig]])
async def page(
        page_index: int = Query(default=1, alias="pageIndex"),
        page_size: int = Query(default=10, alias="pageSize"),
        config_name: Optional[str] = Query(default=None, alias="configName", title="配置名称"),
        config_type: Optional[str] = Query(default=None, alias="configType", title="配置类型"),
        config_key: Optional[str] = Query(default=None, alias="configKey", title="配置键名"),
        config_value: Optional[str] = Query(default=None, alias="configValue", title="配置键值"),
):
    query = SysConfig(
        config_name=config_name,
        config_type=config_type,
        config_key=config_key,
        config_value=config_value,
    )
    data = config_service.page(query, PageData(page_index=page_index, page_size=page_size))
    return ResponseData.success(data)


@router.get("/{id}", tags=["configs"], response_model=ResponseData[SysConfig])
async def get_info(id: int):
    return ResponseData.success(config_service.get_by_id(id))


@router.post("", tags=['configs'], response_model=ResponseData[SysConfig])
async def create(config: SysConfig):
    return ResponseData.success(config_service.create(config))


@router.put("", tags=['configs'], response_model=ResponseData[SysConfig])
async def update(config: SysConfig):
    return ResponseData.success(config_service.update(config))


@router.delete("", tags=['configs'], response_model=ResponseData)
async def delete(id: str = Query(title="ID")):
    list = [int(f) for f in id.split(",")]
    config_service.batch_delete(list)
    return ResponseData.success()
