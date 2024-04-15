import contextvars
from functools import wraps

from middlewares.database import SessionLocal

db_session_context = contextvars.ContextVar("db_session", default=None)


def transactional(read_only: bool = False):
    def decorator(func):
        @wraps(func)
        def wrap_func(*args, **kwargs):
            db_session = db_session_context.get()
            if db_session:
                return func(*args, **kwargs)
            db_session = SessionLocal()
            db_session_context.set(db_session)
            try:
                result = func(*args, **kwargs)
                if not read_only:
                    db_session.commit()
            except Exception as e:
                if not read_only:
                    db_session.rollback()
                raise e
            finally:
                db_session.close()
                db_session_context.set(None)
            return result

        return wrap_func

    return decorator


def db(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session = db_session_context.get()
        return func(*args, **kwargs, db=db_session)

    return wrap_func
