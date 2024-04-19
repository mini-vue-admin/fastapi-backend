from typing import List, Optional

from middlewares.transactional import transactional
from models import PageData
from models.system.schemas import SysConfig
from repository.system import config_repo
from utils import BusinessException


@transactional()
def get_by_id(id):
    return config_repo.get_by_id(id)


def get_config_value(config_key, default: str = None) -> Optional[str]:
    result = config_repo.get_by_config_key(config_key)
    return result.config_value if result is not None else default


@transactional()
def list(query):
    return config_repo.list(query)


@transactional()
def page(query, pg: PageData):
    return config_repo.page(query, pg)


def __validate__(config: SysConfig):
    data = config_repo.get_by_config_key(config.config_key)
    if data is not None:
        if config.id is None or config.id != data.id:
            raise BusinessException(f"参数键名已被注册: {config.config_key}")


@transactional()
def create(config):
    __validate__(config)
    return config_repo.create(config)


@transactional()
def update(config):
    __validate__(config)
    return config_repo.update(config)


@transactional()
def batch_delete(id_list: List[int]):
    return config_repo.batch_delete(id_list)
