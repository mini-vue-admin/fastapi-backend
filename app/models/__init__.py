import json
from typing import Union, TypeVar, Generic, List

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

T = TypeVar('T')


class ResponseData(BaseModel, Generic[T]):
    code: int
    msg: Union[str, None] = Field(default=None)
    data: Union[T, None] = Field(default=None)

    @staticmethod
    def success(data: Union[T, None] = None):
        return ResponseData[T](code=0, msg="success", data=data)

    @staticmethod
    def fail(code: int = 500, msg: str = "Operation failed"):
        return ResponseData(code=code, msg=msg, data=None)


class PageData(BaseModel, Generic[T]):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    list: List[T] = []
    total: int = 0
    page_index: int = 1
    page_size: int = 10