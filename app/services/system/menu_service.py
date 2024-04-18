from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from repository.system import menu_repo


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
        menu.children = list_by_parent_id(menu.id)
    return menus


@transactional()
def get_by_id(id):
    return menu_repo.get_by_id(id)


@transactional()
def create(menu):
    menu_repo.create(menu)
    return menu
