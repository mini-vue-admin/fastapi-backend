from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system.schemas import RoleMember, RoleMenu, SysUser
from repository.system import role_repo
from utils import BusinessException


@transactional()
def get_by_id(id):
    return role_repo.get_by_id(id)


@transactional()
def list(query):
    return role_repo.list(query)


@transactional()
def page(query, pg: PageData):
    return role_repo.page(query, pg)


def __validate__(role):
    data = role_repo.get_by_role_key(role.role_key)
    if data is not None:
        if role.id is None or role.id != data.id:
            raise BusinessException(f"角色键名已被使用: {role.role_key}")


@transactional()
def create(role):
    __validate__(role)
    return role_repo.create(role)


@transactional()
def update(role):
    __validate__(role)
    return role_repo.update(role)


@transactional()
def delete(id):
    role_repo.del_member_by_role(id)
    role_repo.del_menu_by_role(id)
    return role_repo.delete(id)


@transactional()
def batch_delete(id_list: List[int]):
    for id in id_list:
        delete(id)


@transactional()
def member_page(query: SysUser, pg: PageData):
    return role_repo.member_page(query, pg)


@transactional()
def add_member(members: RoleMember):
    for uid in members.member_id:
        role_repo.add_member(members.role_id, uid)


@transactional()
def del_member(role_id, id_list):
    for uid in id_list:
        role_repo.del_member(role_id, uid)


@transactional()
def add_menu(members: RoleMenu):
    role_repo.del_menu_by_role(members.role_id)
    for mid in members.menu_id:
        role_repo.add_menu(members.role_id, mid)


@transactional()
def list_menu(role_id):
    return role_repo.list_menu(role_id)
