from enum import Enum


class DelFlag(Enum):
    """
    是否删除常量
    """
    UN_DELETE = 0
    DELETED = 1


class Status(Enum):
    ENABLED = 0
    DISABLED = 1
