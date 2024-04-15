from typing import Union, TypeVar, Generic, List

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

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


class PageData(BaseModel, Generic[T]):
    model_config = ConfigDict(alias_generator=to_camel)

    list: List[T]
    total: int
    page_num: int
    page_size: int