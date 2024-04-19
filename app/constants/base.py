from enum import Enum

# 部门和菜单的根节点ID
ROOT_PARENT_ID = -1


class DelFlag(Enum):
    """
    是否删除常量
    """
    UN_DELETE = 0
    DELETED = 1


class Status(Enum):
    ENABLED = 0
    DISABLED = 1
