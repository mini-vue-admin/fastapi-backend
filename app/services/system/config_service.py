from typing import List

from middlewares.transactional import transactional
from models import PageData
from repository.system import config_repo


@transactional()
def get_by_id(id):
    return config_repo.get_by_id(id)


@transactional()
def list(query):
    return config_repo.list(query)


@transactional()
def page(query, pg: PageData):
    return config_repo.page(query, pg)


@transactional()
def create(config):
    return config_repo.create(config)


@transactional()
def update(config):
    return config_repo.update(config)


@transactional()
def batch_delete(id_list: List[int]):
    return config_repo.batch_delete(id_list)
