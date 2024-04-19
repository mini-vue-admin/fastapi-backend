from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from repository.system import dict_data_repo
from utils import BusinessException


@transactional()
def get_by_id(id):
    return dict_data_repo.get_by_id(id)


@transactional()
def list_by_type(dict_type):
    return dict_data_repo.list_by_type(dict_type)


@transactional()
def list(query: schemas.SysDictData):
    return dict_data_repo.list(query)


@transactional()
def page(query: schemas.SysDictData, pg: PageData):
    return dict_data_repo.page(query, pg)


def __validate__(dict_data: schemas.SysDictData):
    data = dict_data_repo.get_by_type_and_label(dict_data.dict_type, dict_data.dict_label)
    if data is not None:
        if dict_data is None or dict_data.id != data.id:
            raise BusinessException(f"字典标签已被注册: {data.dict_label}")

    data = dict_data_repo.get_by_type_and_value(dict_data.dict_type, dict_data.dict_value)
    if data is not None:
        if dict_data is None or dict_data.id != data.id:
            raise BusinessException(f"字典键值已被注册: {data.dict_value}")


@transactional()
def create(dict_data: schemas.SysDictData):
    __validate__(dict_data)
    return dict_data_repo.create(dict_data)


@transactional()
def update(dict_data: schemas.SysDictData):
    __validate__(dict_data)
    return dict_data_repo.update(dict_data)


@transactional()
def batch_delete(id_list: List[int]):
    return dict_data_repo.batch_delete(id_list)
