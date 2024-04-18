from typing import List

from sqlalchemy import func, asc
from sqlalchemy.orm import Session

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysMenu
from utils.common import not_none_or_blank


@db
# 分页查询方法
def page(params: schemas.SysMenu, page: PageData, db):
    offset = (page.page_index - 1) * page.page_size
    total_count = db.query(func.count(SysMenu.id)).query_by(build_query(params)).scalar()
    items = (db.query(SysMenu)
             .query_by(build_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


@db
def list(params, db):
    return db.query(SysMenu).query_by(build_query(params)).all()


@db
def list_by_parent_id(parent_id, db):
    return list(schemas.SysMenu(parent_id=parent_id))


def build_query(params: schemas.SysMenu):
    def warp(query):
        return (
            query
            .filter_if(not_none_or_blank(params.parent_id), SysMenu.parent_id == params.parent_id)
            .filter_if(not_none_or_blank(params.menu_type), SysMenu.menu_type == params.menu_type)
            .filter_if(not_none_or_blank(params.status), SysMenu.status == params.status)
            .filter_if(not_none_or_blank(params.menu_name), SysMenu.menu_name.like(f"%{params.menu_name}%"))
            .filter_if(not_none_or_blank(params.menu_title), SysMenu.menu_title.like(f"%{params.menu_title}%"))
            .filter_if(not_none_or_blank(params.path), SysMenu.path.like(f"%{params.path}%"))
            .filter_if(not_none_or_blank(params.component), SysMenu.component.like(f"%{params.component}%"))
            .order_by(asc(SysMenu.order_num))
        )

    return warp


@db
def get_by_id(id, db):
    return db.query(SysMenu).filter(SysMenu.id == id).first()


@db
def create(menu: schemas.SysMenu, db):
    model = SysMenu(**menu.dict(exclude="children"))
    db.add(model)
    return model


@db
def update(menu: schemas.SysMenu, db: Session):
    db.query(SysMenu).filter(SysMenu.id == menu.id).update(menu.dict(exclude_none=True))
    return db.query(SysMenu).filter(SysMenu.id == menu.id).first()


@db
def batch_delete(id_list: List[int], db: Session):
    return db.query(SysMenu).filter(SysMenu.id.in_(id_list)).delete()
