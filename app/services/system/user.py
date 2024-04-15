from middlewares.transactional import transactional
from models.system import models
from models.system.schemas import User
from repository.system import user


class UserService:

    def __init__(self):
        pass

    # TODO
    def authenticate_user(self, username, password, ) -> User:
        pass

    @transactional(read_only=True)
    def list(self) -> models.User:
        return user.list()

    @transactional(read_only=False)
    def get_by_id(self, id) -> models.User:
        user.update(1, {"nickname":"Best"})
        return user.get_by_id(id)
