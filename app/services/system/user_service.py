from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system.schemas import SysUser
from repository.system import user_repo


# TODO
def authenticate_user(username, password, ) -> SysUser:
    pass


@transactional()
def get_by_id(id):
    return user_repo.get_by_id(id)


@transactional()
def list(query):
    return user_repo.list(query)


@transactional()
def page(query, pg: PageData):
    return user_repo.page(query, pg)


@transactional()
def create(user):
    return user_repo.create(user)


@transactional()
def update(user):
    return user_repo.update(user)


@transactional()
def batch_delete(id_list: List[int]):
    return user_repo.batch_delete(id_list)
