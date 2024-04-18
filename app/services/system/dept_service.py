from typing import List

from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from models.system.schemas import DeptMember
from repository.system import dept_repo


@transactional()
def get_by_id(id):
    return dept_repo.get_by_id(id)


@transactional()
def list(query):
    return dept_repo.list(query)


@transactional()
def list_by_parent_id(parent_id):
    return dept_repo.list_by_parent_id(parent_id)


@transactional()
def page(query, pg: PageData):
    return dept_repo.page(query, pg)


@transactional()
def tree(query):
    depts = dept_repo.list(query)
    for dept in depts:
        dept.children = tree(schemas.SysDept(parent_id=dept.id))
    return depts


@transactional()
def create(dept):
    return dept_repo.create(dept)


@transactional()
def update(dept):
    return dept_repo.update(dept)


@transactional()
def batch_delete(id_list: List[int]):
    return dept_repo.batch_delete(id_list)


@transactional()
def add_member(members: DeptMember):
    for uid in members.member_id:
        dept_repo.add_member(members.dept_id, uid)


@transactional()
def del_member(dept_id, id_list):
    for uid in id_list:
        dept_repo.del_member(dept_id, uid)
