import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, field_serializer, ConfigDict
from pydantic.alias_generators import to_camel


# 定义一个包含公共字段的基类
class BaseModelWithCommonFields(BaseModel):
    # https://blog.csdn.net/weixin_43701894/article/details/132279518
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: int
    del_flag: int
    create_by: Union[str, None]
    create_time: Union[datetime.datetime, None]
    update_by: Union[str, None]
    update_time: Union[datetime.datetime, None]


    @field_serializer('create_time')
    def serialize_ct(self, dt: datetime.datetime, _info):
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')


    @field_serializer('update_time')
    def serialize_ut(self, dt: datetime.datetime, _info):
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')


# 定义具体的User模型，继承自BaseModelWithCommonFields
class User(BaseModelWithCommonFields):
    dept_id: Optional[int]
    username: str
    nickname: str
    email: Optional[str]
    phonenumber: Optional[str]
    sex: str
    avatar: Optional[str]
    password: str
    status: str
    login_ip: Optional[str]
    login_date: Optional[datetime.datetime]

    @field_serializer('login_date')
    def serialize_ld(self, dt: datetime.datetime, _info):
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')