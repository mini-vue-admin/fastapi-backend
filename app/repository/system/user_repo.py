from fastapi import HTTPException
from sqlalchemy import func, desc

from middlewares.transactional import db
from models import PageData
from models.system import schemas
from models.system.models import SysUser


# 假设我们已经有了一个Base和User类，如下所示：
# from middlewares.database import Base
# class User(Base, BaseMixin):
#     __tablename__ = 'sys_user'
#     ...

@db
def get_by_id(user_id, db):
    return db.query(SysUser).filter(SysUser.id == user_id).first()


# CRUD操作: 创建
@db
def create(db, user_data, ):
    new_user = SysUser(**user_data)
    db.add(new_user)
    return new_user


@db
def list(db) -> SysUser:
    return db.query(SysUser).all()


@db
# CRUD操作: 更新
def update(user_id, update_data, db):
    user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if user:
        for key, value in update_data.items():
            setattr(user, key, value)
    else:
        raise HTTPException(status_code=500, detail="user not exists")


@db
# CRUD操作: 删除
def delete(db, user_id):
    user = db.query(SysUser).filter(SysUser.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    else:
        return False


@db
# 分页查询方法
def page(user: schemas.SysUser, page: PageData, db):
    offset = (page.page_num - 1) * page.page_size
    total_count = db.query(func.count(SysUser.id)).scalar()
    items = (db.query(SysUser)
             .filter()
             .order_by(desc(SysUser.create_time))
             .offset(offset)
             .limit(page.page_size))
    return PageData(list=items, total=total_count, pageNum=page.page_num, pageSize=page.page_size)
