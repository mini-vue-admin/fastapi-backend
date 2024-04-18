from middlewares.transactional import transactional
from models import PageData
from models.system import models
from models.system.schemas import SysUser
from repository.system import user_repo


# TODO
def authenticate_user(username, password, ) -> SysUser:
    pass


@transactional()
def list() -> models.SysUser:
    return user_repo.list()


@transactional()
def get_by_id(id) -> models.SysUser:
    user_repo.update(1, {"nickname": "Best"})
    return user_repo.get_by_id(id)


@transactional()
def page(user: SysUser, pg: PageData) -> PageData[SysUser]:
    return user_repo.page(user, pg)
