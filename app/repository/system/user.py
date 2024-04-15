from fastapi import HTTPException
from sqlalchemy import func

from middlewares.transactional import db
from models import PageData
from models.system.models import User


# 假设我们已经有了一个Base和User类，如下所示：
# from middlewares.database import Base
# class User(Base, BaseMixin):
#     __tablename__ = 'sys_user'
#     ...

@db
def get_by_id(user_id, db):
    return db.query(User).filter(User.id == user_id).first()


# CRUD操作: 创建
@db
def create(db, user_data, ):
    new_user = User(**user_data)
    db.add(new_user)
    return new_user


@db
def list(db) -> User:
    return db.query(User).all()


@db
# CRUD操作: 更新
def update(user_id, update_data, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in update_data.items():
            setattr(user, key, value)
    else:
        raise HTTPException(status_code=500, detail="user not exists")


@db
# CRUD操作: 删除
def delete(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    else:
        return False


@db
# 分页查询方法
def page(db, page, per_page):
    total_count = db.query(func.count(User.id)).scalar()
    items = db.query(User).paginate(page, per_page, False).items
    return PageData(list=items, total=total_count, pageNum=page, pageSize=per_page)
