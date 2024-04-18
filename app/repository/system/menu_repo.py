from sqlalchemy import func, desc

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysMenu
from utils.common import not_none_or_blank


@db
# 分页查询方法
def page(params: schemas.SysMenu, page: PageData, db):
    offset = (page.page_num - 1) * page.page_size
    total_count = db.query(func.count(SysMenu.id)).query_by(build_query(params)).scalar()
    items = (db.query(SysMenu)
             .query_by(build_query(params))
             .order_by(desc(SysMenu.create_time))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, pageNum=page.page_num, pageSize=page.page_size)


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
        )

    return warp


@db
def get_by_id(id, db):
    return db.query(SysMenu).filter(SysMenu.id == id).first()

@db
def create(menu, db):
    model = SysMenu(**menu.dict())
    db.add(model)

