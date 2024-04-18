from typing import List

from sqlalchemy import func, or_, asc
from sqlalchemy.orm import Session

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysUser
from utils.common import not_none_or_blank


@db
def get_by_id(id, db):
    return db.query(SysUser).filter(SysUser.id == id).first()


@db
def list(params: schemas.SysUser, db):
    return db.query(SysUser).query_by(build_query(params)).all()


@db
def page(params: schemas.SysUser, page: PageData, db):
    offset = (page.page_index - 1) * page.page_size
    total_count = db.query(func.count(SysUser.id)).query_by(build_query(params)).scalar()
    items = (db.query(SysUser)
             .query_by(build_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


def build_query(params: schemas.SysUser):
    def warp(query):
        return (query
                .filter_if(not_none_or_blank(params.dept_id), SysUser.dept_id == params.dept_id)
                .filter_if(not_none_or_blank(params.username), SysUser.username.like(f"%{params.username}%"))
                .filter_if(not_none_or_blank(params.nickname), SysUser.nickname.like(f"%{params.nickname}%"))
                .filter_if(not_none_or_blank(params.email), SysUser.email.like(f"%{params.email}%"))
                .filter_if(not_none_or_blank(params.phonenumber), SysUser.phonenumber.like(f"%{params.phonenumber}%"))
                .filter_if(not_none_or_blank(params.status), SysUser.status == params.status)
                .filter_if(not_none_or_blank(params.params['keyword']), or_(
            SysUser.username.like(f"%{params.params['keyword']}%"),
            SysUser.nickname.like(f"%{params.params['keyword']}%"),
            SysUser.email.like(f"%{params.params['keyword']}%"),
            SysUser.phonenumber.like(f"%{params.params['keyword']}%")
        ))
                .filter_if(not_none_or_blank(params.params['dis_dept_id']), or_(
            SysUser.dept_id != params.params['dis_dept_id'],
            SysUser.dept_id.is_(None)
        ))
                .order_by(asc(SysUser.username))
                )

    return warp


@db
def create(user: schemas.SysUser, db):
    model = SysUser(**user.dict())
    db.add(model)
    return model


@db
def update(user: schemas.SysUser, db: Session):
    db.query(SysUser).filter(SysUser.id == user.id).update(user.dict(exclude_none=True))
    return db.query(SysUser).filter(SysUser.id == user.id).first()


@db
def batch_delete(id_list: List[int], db: Session):
    return db.query(SysUser).filter(SysUser.id.in_(id_list)).delete()
