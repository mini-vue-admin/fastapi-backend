from typing import List

from constants.sys_config_keys import INIT_PASSWORD
from middlewares.transactional import transactional
from models import PageData
from models.system.schemas import SysUser
from repository.system import user_repo, role_repo, config_repo
from utils import BusinessException


@transactional()
def authenticate_user(username, password, ) -> SysUser:
    user = user_repo.get_by_username(username)
    if (user.password == password):
        return user
    else:
        raise BusinessException(f'用户登录失败：{username}')


@transactional()
def get_by_id(id):
    return user_repo.get_by_id(id)

@transactional()
def get_by_username(username):
    return user_repo.get_by_username(username)

@transactional()
def list(query):
    return user_repo.list(query)


@transactional()
def page(query, pg: PageData):
    return user_repo.page(query, pg)


def __validate__(user):
    data = user_repo.get_by_username(user.username)
    if data is not None:
        if user.id is None or user.id != data.id:
            raise BusinessException(f"用户名已被使用: {user.username}")


@transactional()
def create(user):
    __validate__(user)
    data = user_repo.create(user)
    reset_pwd(user.id)
    return data


@transactional()
def update(user):
    __validate__(user)
    return user_repo.update(user)


@transactional()
def reset_pwd(uid):
    config = config_repo.get_by_config_key(INIT_PASSWORD)
    return user_repo.update_pwd(uid, config.config_value)


@transactional()
def batch_delete(id_list: List[int]):
    for id in id_list:
        role_repo.del_member_by_user(id)
    return user_repo.batch_delete(id_list)
