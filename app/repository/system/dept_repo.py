from typing import List

from sqlalchemy import func, asc
from sqlalchemy.orm import Session

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysDept, SysUser
from utils.common import not_none_or_blank


@db
def get_by_id(id, db):
    return db.query(SysDept).filter(SysDept.id == id).first()


@db
def list(params: schemas.SysDept, db):
    return db.query(SysDept).query_by(build_query(params)).all()


@db
def list_by_parent_id(parent_id, db):
    return db.query(SysDept).filter(SysDept.parent_id == parent_id).all()


@db
def page(params: schemas.SysDept, page: PageData, db):
    offset = (page.page_index - 1) * page.page_size
    total_count = db.query(func.count(SysDept.id)).query_by(build_query(params)).scalar()
    items = (db.query(SysDept)
             .query_by(build_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


def build_query(params: schemas.SysDept):
    def warp(query):
        return (query
                .filter_if(not_none_or_blank(params.dept_name), SysDept.dept_name.like(f"%{params.dept_name}%"))
                .filter_if(not_none_or_blank(params.parent_id), SysDept.parent_id == params.parent_id)
                .order_by(asc(SysDept.order_num))
                )

    return warp


@db
def create(dept, db):
    model = SysDept(**dept.dict(exclude="children"))
    db.add(model)
    return model


@db
def update(dept: schemas.SysDept, db: Session):
    db.query(SysDept).filter(SysDept.id == dept.id).update(dept.dict(exclude_none=True))
    return db.query(SysDept).filter(SysDept.id == dept.id).first()


@db
def batch_delete(id_list: List[int], db: Session):
    return db.query(SysDept).filter(SysDept.id.in_(id_list)).delete()


@db
def add_member(dept_id, uid, db):
    db.query(SysUser).filter(SysUser.id == uid).update({"dept_id": dept_id})


@db
def del_member(dept_id, uid, db):
    db.query(SysUser).filter(SysUser.id == uid).update({"dept_id": None})
