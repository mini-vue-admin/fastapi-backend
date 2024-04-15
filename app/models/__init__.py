from typing import Union, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class ResponseData(BaseModel, Generic[T]):
    code: int
    msg: Union[str, None] = None
    data: Union[T, None] = None

    @staticmethod
    def success(data: Union[T, None] = None):
        return ResponseData(code=0, msg="success", data=data)

    @staticmethod
    def fail(code: int = 500, msg: str = "Operation failed"):
        return ResponseData(code=code, msg=msg, data=None)
