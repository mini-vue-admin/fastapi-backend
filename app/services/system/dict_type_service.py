from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from repository.system import dict_type_repo, dict_data_repo
from utils import BusinessException


@transactional()
def get_by_id(id):
    return dict_type_repo.get_by_id(id)


@transactional()
def list(query: schemas.SysDictType):
    return dict_type_repo.list(query)


@transactional()
def page(query: schemas.SysDictType, pg: PageData):
    return dict_type_repo.page(query, pg)


def __validate__(dict_type: schemas.SysDictType):
    data = dict_type_repo.get_by_dict_type(dict_type.dict_type)
    if data is not None:
        if dict_type.id is None or dict_type.id != data.id:
            raise BusinessException(f"字典类型已被注册: {dict_type.dict_type}")


@transactional()
def create(dict_type: schemas.SysDictType):
    __validate__(dict_type)
    return dict_type_repo.create(dict_type)


@transactional()
def update(dict_type: schemas.SysDictType):
    __validate__(dict_type)
    return dict_type_repo.update(dict_type)


@transactional()
def batch_delete(id_list: List[int]):
    for id in id_list:
        dict_type = get_by_id(id)
        if dict_type is not None:
            dict_data_repo.delete_by_dict_type(dict_type.dict_type)

    return dict_type_repo.batch_delete(id_list)
