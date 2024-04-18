import contextvars
from functools import wraps
from typing import Optional, Callable

from sqlalchemy.orm import Session

from middlewares.database import SessionLocal

db_session_context = contextvars.ContextVar("db_session", default=None)

from sqlalchemy.orm import Query


class CustomQuery(Query):
    def filter_if(self: Query, condition: bool, *criterion):
        if condition:
            return self.filter(*criterion)
        else:
            return self

    def query_by(self, builder: Callable):
        return builder(self)


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
