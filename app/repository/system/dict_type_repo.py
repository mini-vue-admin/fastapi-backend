from typing import List

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysDictType
from utils.common import not_none_or_blank


@db
def get_by_id(id, db):
    return db.query(SysDictType).filter(SysDictType.id == id).first()


@db
def get_by_dict_type(dict_type, db):
    return db.query(SysDictType).filter(SysDictType.dict_type == dict_type).first()


@db
def list(params: schemas.SysDictType, db):
    return db.query(SysDictType).query_by(build_query(params)).all()


@db
def page(params: schemas.SysDictType, page: PageData, db):
    offset = (page.page_index - 1) * page.page_size
    total_count = db.query(func.count(SysDictType.id)).query_by(build_query(params)).scalar()
    items = (db.query(SysDictType)
             .query_by(build_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


def build_query(params: schemas.SysDictType):
    def warp(query):
        return (query
                .filter_if(not_none_or_blank(params.dict_type), SysDictType.dict_type.like(f"%{params.dict_type}%"))
                .filter_if(not_none_or_blank(params.dict_name), SysDictType.dict_name.like(f"%{params.dict_name}%"))
                .order_by(desc(SysDictType.create_time))
                )

    return warp


@db
def create(dict_type: schemas.SysDictType, db):
    model = SysDictType(**dict_type.dict())
    db.add(model)
    return model


@db
def update(dict_type: schemas.SysDictType, db: Session):
    db.query(SysDictType).filter(SysDictType.id == dict_type.id).update(dict_type.dict(exclude_none=True))
    return db.query(SysDictType).filter(SysDictType.id == dict_type.id).first()


@db
def batch_delete(id_list: List[int], db: Session):
    return db.query(SysDictType).filter(SysDictType.id.in_(id_list)).delete()
