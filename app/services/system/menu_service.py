from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from repository.system import menu_repo, role_repo
from utils import BusinessException


@transactional()
def list(query: schemas.SysMenu):
    return menu_repo.list(query)


@transactional()
def page(menu: schemas.SysMenu, pg: PageData):
    return menu_repo.page(menu, pg)


@transactional()
def list_by_parent_id(parent_id):
    return menu_repo.list_by_parent_id(parent_id)


@transactional()
def tree(query: schemas.SysMenu):
    menus = menu_repo.list(query)
    for menu in menus:
        menu.children = tree(schemas.SysMenu(parent_id=menu.id))
    return menus


@transactional()
def get_by_id(id):
    return menu_repo.get_by_id(id)


def __validate__(menu):
    if menu.parent_id == menu.id:
        raise BusinessException("禁止设置自身为父级节点")


@transactional()
def create(menu):
    __validate__(menu)
    return menu_repo.create(menu)


@transactional()
def update(menu: schemas.SysMenu):
    __validate__(menu)
    return menu_repo.update(menu)


@transactional()
def batch_delete(id_list: List[int]):
    for id in id_list:
        delete(id)


@transactional()
def delete(id):
    children = list_by_parent_id(id)
    for child in children:
        delete(child.id)
    role_repo.del_menu_by_menu(id)
    menu_repo.delete(id)
