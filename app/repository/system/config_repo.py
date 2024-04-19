from typing import List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysConfig
from utils.common import not_none_or_blank


@db
def get_by_id(id, db):
    return db.query(SysConfig).filter(SysConfig.id == id).first()


@db
def list(params: schemas.SysConfig, db):
    return db.query(SysConfig).query_by(build_query(params)).all()


@db
def page(params: schemas.SysConfig, page: PageData, db):
    offset = (page.page_index - 1) * page.page_size
    total_count = db.query(func.count(SysConfig.id)).query_by(build_query(params)).scalar()
    items = (db.query(SysConfig)
             .query_by(build_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


def build_query(params: schemas.SysConfig):
    def warp(query):
        return (query
                .filter_if(not_none_or_blank(params.config_name), SysConfig.config_name.like(f"%{params.config_name}%"))
                .filter_if(not_none_or_blank(params.config_type), SysConfig.config_type == params.config_type)
                .filter_if(not_none_or_blank(params.config_key), SysConfig.config_key.like(f"%{params.config_key}%"))
                .filter_if(not_none_or_blank(params.config_value),
                           SysConfig.config_value.like(f"%{params.config_value}%"))
                .order_by(desc(SysConfig.create_time))
                )

    return warp


@db
def create(config, db):
    model = SysConfig(**config.dict())
    db.add(model)
    return model


@db
def update(config: schemas.SysConfig, db: Session):
    db.query(SysConfig).filter(SysConfig.id == config.id).update(config.dict(exclude_none=True))
    return db.query(SysConfig).filter(SysConfig.id == config.id).first()


@db
def batch_delete(id_list: List[int], db: Session):
    return db.query(SysConfig).filter(SysConfig.id.in_(id_list)).delete()


@db
def get_by_config_key(config_key, db):
    return db.query(SysConfig).filter(SysConfig.config_key == config_key).first()
