from typing import List

from sqlalchemy import func, desc, or_, asc
from sqlalchemy.orm import Session

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysRole, SysRoleUser, SysRoleMenu, SysUser, SysMenu
from utils.common import not_none_or_blank


@db
def get_by_id(id, db):
    return db.query(SysRole).filter(SysRole.id == id).first()


@db
def get_by_role_key(role_key, db):
    return db.query(SysMenu).filter(SysRole.role_key == role_key).first()


@db
def list(params: schemas.SysRole, db):
    return db.query(SysRole).query_by(build_query(params)).all()


@db
def page(params: schemas.SysRole, page: PageData, db):
    offset = (page.page_index - 1) * page.page_size
    total_count = db.query(func.count(SysRole.id)).query_by(build_query(params)).scalar()
    items = (db.query(SysRole)
             .query_by(build_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


def build_query(params: schemas.SysRole):
    def warp(query):
        return (query
                .filter_if(not_none_or_blank(params.role_name), SysRole.role_name.like(f"%{params.role_name}%"))
                .filter_if(not_none_or_blank(params.role_key), SysRole.role_key == params.role_key)
                .order_by(desc(SysRole.create_time))
                )

    return warp


@db
def create(role, db):
    model = SysRole(**role.dict())
    db.add(model)
    return model


@db
def update(role: schemas.SysRole, db: Session):
    db.query(SysRole).filter(SysRole.id == role.id).update(role.dict(exclude_none=True))
    return db.query(SysRole).filter(SysRole.id == role.id).first()


@db
def delete(id, db):
    return db.query(SysRole).filter(SysRole.id == id).delete()


@db
def batch_delete(id_list: List[int], db: Session):
    return db.query(SysRole).filter(SysRole.id.in_(id_list)).delete()


@db
def add_member(role_id, uid, db):
    db.add(SysRoleUser(user_id=uid, role_id=role_id))


@db
def del_member(role_id, uid, db):
    db.query(SysRoleUser).filter(SysRoleUser.role_id == role_id).filter(SysRoleUser.user_id == uid).delete()


@db
def del_member_by_user(uid, db):
    db.query(SysRoleUser).filter(SysRoleUser.user_id == uid).delete()


@db
def del_member_by_role(role_id, db):
    db.query(SysRoleUser).filter(SysRoleUser.role_id == role_id).delete()


@db
def add_menu(role_id, mid, db):
    db.add(SysRoleMenu(menu_id=mid, role_id=role_id))


@db
def del_menu(role_id, mid, db):
    db.query(SysRoleMenu).filter(SysRoleMenu.role_id == role_id).filter(SysRoleMenu.menu_id == mid).delete()


@db
def del_menu_by_role(role_id, db):
    db.query(SysRoleMenu).filter(SysRoleMenu.role_id == role_id).delete()


@db
def del_menu_by_menu(mid, db):
    db.query(SysRoleMenu).filter(SysRoleMenu.menu_id == mid).delete()


@db
def member_page(params: SysUser, page: PageData, db: Session):
    total_count: int = db.query(func.count(SysUser.id)).query_by(build_member_query(params)).scalar()
    offset = (page.page_index - 1) * page.page_size
    items = (db.query(SysUser)
             .query_by(build_member_query(params))
             .offset(offset)
             .limit(page.page_size)
             .all())
    return PageData(list=items, total=total_count, page_index=page.page_index, pageSize=page.page_size)


def build_member_query(params: SysUser):
    def warp(query):
        return (
            query
            .join(SysRoleUser, SysRoleUser.user_id == SysUser.id, isouter=True)
            .filter_if(not_none_or_blank(params.username), SysUser.username.like(f"%{params.username}%"))
            .filter_if(not_none_or_blank(params.nickname), SysUser.nickname.like(f"%{params.nickname}%"))
            .filter_if(not_none_or_blank(params.email), SysUser.email.like(f"%{params.email}%"))
            .filter_if(not_none_or_blank(params.phonenumber), SysUser.phonenumber.like(f"%{params.phonenumber}%"))
            .filter_if(not_none_or_blank(params.status), SysUser.status == params.status)

            .filter_if(not_none_or_blank(params.params['role_id']), SysRoleUser.role_id == params.params['role_id'])
            .filter_if(not_none_or_blank(params.params['dis_role_id']),
                       or_(SysRoleUser.role_id != params.params['dis_role_id'], SysRoleUser.role_id.is_(None)))

            .filter_if(not_none_or_blank(params.params['keyword']), or_(
                SysUser.username.like(f"%{params.params['keyword']}%"),
                SysUser.nickname.like(f"%{params.params['keyword']}%"),
                SysUser.email.like(f"%{params.params['keyword']}%"),
                SysUser.phonenumber.like(f"%{params.params['keyword']}%")
            ))
            .distinct()
            .order_by(asc(SysUser.username))
        )

    return warp


@db
def list_menu(role_id, db):
    return db.query(SysMenu).join(SysRoleMenu, SysMenu.id == SysRoleMenu.menu_id).filter(
        SysRoleMenu.role_id == role_id).order_by(asc(SysMenu.order_num)).all()
