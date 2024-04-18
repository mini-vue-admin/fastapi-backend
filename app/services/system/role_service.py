from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system.schemas import RoleMember, RoleMenu, SysUser
from repository.system import role_repo


@transactional()
def get_by_id(id):
    return role_repo.get_by_id(id)


@transactional()
def list(query):
    return role_repo.list(query)


@transactional()
def page(query, pg: PageData):
    return role_repo.page(query, pg)


@transactional()
def create(role):
    return role_repo.create(role)


@transactional()
def update(role):
    return role_repo.update(role)


@transactional()
def batch_delete(id_list: List[int]):
    return role_repo.batch_delete(id_list)


@transactional()
def add_member(members: RoleMember):
    for uid in members.member_id:
        role_repo.add_member(members.role_id, uid)


@transactional()
def del_member(role_id, id_list):
    for uid in id_list:
        role_repo.del_member(role_id, uid)


@transactional()
def member_page(query: SysUser, pg: PageData):
    return role_repo.member_page(query, pg)


@transactional()
def add_menu(members: RoleMenu):
    role_repo.del_menu_by_role(members.role_id)
    for mid in members.menu_id:
        role_repo.add_menu(members.role_id, mid)


@transactional()
def list_menu(role_id):
    return role_repo.list_menu(role_id)
