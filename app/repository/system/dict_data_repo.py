from typing import List

from sqlalchemy import func, asc
from sqlalchemy.orm import Session

from constants.base import DelFlag
from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysDictData
from utils.common import not_none_or_blank


@db
def get_by_id(id, db):
    return db.query(SysDictData).filter(SysDictData.id == id).one_or_none()


@db
def get_by_type_and_value(type, value, db):
    return db.query(SysDictData).filter(SysDictData.dict_type == type).filter(SysDictData.dict_value == value).one_or_none()


@db
def get_by_type_and_label(type, label, db):
    return db.query(SysDictData).filter(SysDictData.dict_type == type).filter(SysDictData.dict_label == label).one_or_none()


@db
def list_by_type(dict_type, db):
    return db.query(SysDictData).filter(SysDictData.dict_type == dict_type).order_by(asc(SysDictData.order_num)).all()


@db
def list(params: schemas.SysDictData, db):
    return db.query(SysDictData).query_by(build_query(params)).all()


@db
def page(params: schemas.SysDictData, page: PageData, db):
    offset = (page.page_index - 1) * page.page_size
    total_count = db.query(func.count(SysDictData.id)).query_by(build_query(params)).undeleted().scalar()
    items = (db.query(SysDictData)
             .query_by(build_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


def build_query(params: schemas.SysDictData):
    def warp(query):
        return (query
                .filter_if(not_none_or_blank(params.dict_type), SysDictData.dict_type == params.dict_type)
                .filter_if(not_none_or_blank(params.dict_value), SysDictData.dict_value == params.dict_value)
                .filter_if(not_none_or_blank(params.dict_label), SysDictData.dict_label.like(f"%{params.dict_label}%"))
                .order_by(asc(SysDictData.order_num))
                )

    return warp


@db
def create(dict_data: schemas.SysDictData, db):
    model = SysDictData(**dict_data.dict())
    db.add(model)
    return model


@db
def update(dict_data: schemas.SysDictData, db: Session):
    db.query(SysDictData).filter(SysDictData.id == dict_data.id).update(dict_data.dict(exclude_none=True))
    return db.query(SysDictData).filter(SysDictData.id == dict_data.id).one_or_none()


@db
def batch_delete(id_list: List[int], db: Session):
    return db.query(SysDictData).filter(SysDictData.id.in_(id_list)).update({'del_flag': DelFlag.DELETED.value})


@db
def delete_by_dict_type(dict_type, db):
    return db.query(SysDictData).filter(SysDictData.dict_type == dict_type).update({'del_flag': DelFlag.DELETED.value})
