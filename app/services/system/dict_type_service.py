from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from repository.system import dict_type_repo


@transactional()
def get_by_id(id):
    return dict_type_repo.get_by_id(id)


@transactional()
def list(query: schemas.SysDictType):
    return dict_type_repo.list(query)


@transactional()
def page(query: schemas.SysDictType, pg: PageData):
    return dict_type_repo.page(query, pg)


@transactional()
def create(dict_type: schemas.SysDictType):
    return dict_type_repo.create(dict_type)


@transactional()
def update(dict_type: schemas.SysDictType):
    return dict_type_repo.update(dict_type)


@transactional()
def batch_delete(id_list: List[int]):
    return dict_type_repo.batch_delete(id_list)
