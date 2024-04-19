import contextvars
from functools import wraps
from typing import Optional, Callable

from sqlalchemy.orm import Session

from constants.base import DelFlag
from middlewares.database import SessionLocal
from models.system.models import BaseMixin

db_session_context = contextvars.ContextVar("db_session", default=None)

from sqlalchemy.orm import Query


def resolve_entities(entities):
    model_cls = []
    if hasattr(entities, '__len__'):
        for entity in entities:
            if isinstance(entity, type) and issubclass(entity, BaseMixin):
                model_cls.append(entity)
    else:
        if isinstance(entities, type) and issubclass(entities, BaseMixin):
            model_cls.append(entities)

    return set(model_cls)


# @event.listens_for(Query, "before_compile", retval=True)
# def no_deleted(query):
#     for desc in query.column_descriptions:
#         entity = desc['entity']
#         if entity:
#             query = query.filter(entity.del_flag == DelFlag.UN_DELETE.value)
#
#     return query


class CustomQuery(Query):
    def __new__(cls, *args, **kwargs):
        """
        实现自动追加逻辑删除查询条件

        原理：
            - 获取查询参数entities，如果是ORM对象，且为BaseMixin的子类，则默认追加逻辑删除的查询条件。
            - 如果构建对象传入了：{'with_deleted': True}，则表示忽略追加逻辑删除查询条件

        注意：该方式仅适用于query(SysUser)类似的直接查询ORM对象的语法，而不适合包含SQL 函数的语法，例如：query(func.count(SysUser.id))

        :param args:
        :param kwargs:
        """
        obj = super(CustomQuery, cls).__new__(cls)

        with_deleted = kwargs.pop('with_deleted', False)
        entities = kwargs.get('entities', None) or args[0] if args else None
        if len(args) > 0:
            super(CustomQuery, obj).__init__(*args, **kwargs)
            if not with_deleted:
                ets = resolve_entities(entities)
                for e in ets:
                    obj = obj.filter(getattr(e, "del_flag") == DelFlag.UN_DELETE.value)

        return obj

    def __init__(self, *args, **kwargs):
        pass

    def filter_if(self: Query, condition: bool, *criterion):
        """
        根据条件判断是否需要添加过滤条件
        :param condition: 如果为True则追加查询语句
        :param criterion: 查询语句
        :return:
        """
        if condition:
            return self.filter(*criterion)
        else:
            return self

    def query_by(self, builder: Callable):
        """
        传入一个构建函数来构建查询条件，方便复用查询条件构造流程
        :param builder:
        :return:
        """
        return builder(self)

    def undeleted(self, cls: BaseMixin = None):
        """
        追加查询条件为未删除项

        因为CustomQuery自动追加的未删除条件只适用于query(SysUser)类似的请求，
        对于查询条件包含函数时：query(func.count(SysUser.id))无法自动追加未删除条件，需要手动调用该方法

        注意：对于join查询，如果存在多个表都有del_flag属性，需要通过cls参数指定映射的对象类名
        :param cls: 对象类名
        :return:
        """
        if cls is None:
            return self.filter_by(del_flag=DelFlag.UN_DELETE.value)
        else:
            return self.filter(getattr(cls, "del_flag") == DelFlag.UN_DELETE.value)


def transactional():
    def decorator(func):
        @wraps(func)
        def wrap_func(*args, **kwargs):
            db_session = db_session_context.get()
            if db_session:
                return func(*args, **kwargs)
            db_session = SessionLocal(query_cls=CustomQuery)
            db_session_context.set(db_session)
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                db_session.rollback()
                raise e
            finally:
                db_session.commit()
                db_session.close()
                db_session_context.set(None)

        return wrap_func

    return decorator


def db(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session: Optional[Session] = db_session_context.get()
        if db_session is None:
            raise Exception("current sqlalchemy session is none")
        else:
            return func(*args, **kwargs, db=db_session)

    return wrap_func
