from typing import List

from constants.base import ROOT_PARENT_ID
from middlewares.transactional import transactional
from models import PageData
from models.system import schemas
from models.system.schemas import DeptMember, SysDept
from repository.system import dept_repo
from utils import BusinessException
from utils.common import is_none_or_blank


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


def __validate__(dept):
    if dept.id == dept.parent_id:
        raise BusinessException("禁止设置自身为父级节点")
    if dept.id is not None and dept.parent_id != ROOT_PARENT_ID:
        parent = dept_repo.get_by_id(dept.parent_id)
        if parent is not None and parent.ancestors.split(",").contains(str(dept.id)):
            raise BusinessException("禁止设置当前节点的子节点为父节点")


def __resolve_ancestor__(dept):
    if dept.parent_id == ROOT_PARENT_ID:
        return ""
    ancestors = dept_repo.get_by_id(dept.parent_id).ancestors
    if is_none_or_blank(ancestors):
        return str(dept.parent_id)
    else:
        return f"{ancestors},{dept.parent_id}"


@transactional()
def create(dept):
    __validate__(dept)
    __resolve_ancestor__(dept)
    return dept_repo.create(dept)


@transactional()
def update(dept):
    __validate__(dept)
    __resolve_ancestor__(dept)
    return dept_repo.update(dept)


@transactional()
def batch_delete(id_list: List[int]):
    dept_repo.batch_del_member_by_dept(id_list)
    return dept_repo.batch_delete(id_list)


@transactional()
def add_member(members: DeptMember):
    for uid in members.member_id:
        dept_repo.add_member(members.dept_id, uid)


@transactional()
def del_member(dept_id, id_list):
    for uid in id_list:
        dept_repo.del_member(dept_id, uid)
