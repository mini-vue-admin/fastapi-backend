from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from repository.system import dict_data_repo


@transactional()
def get_by_id(id):
    return dict_data_repo.get_by_id(id)


@transactional()
def list(query: schemas.SysDictData):
    return dict_data_repo.list(query)


@transactional()
def page(query: schemas.SysDictData, pg: PageData):
    return dict_data_repo.page(query, pg)


@transactional()
def create(dict_data: schemas.SysDictData):
    return dict_data_repo.create(dict_data)


@transactional()
def update(dict_data: schemas.SysDictData):
    return dict_data_repo.update(dict_data)


@transactional()
def batch_delete(id_list: List[int]):
    return dict_data_repo.batch_delete(id_list)
