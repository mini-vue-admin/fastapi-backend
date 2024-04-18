import datetime
from typing import Optional, List

from pydantic import BaseModel, field_serializer, ConfigDict
from pydantic.alias_generators import to_camel


# 定义一个包含公共字段的基类
class BaseModelWithCommonFields(BaseModel):
    # https://blog.csdn.net/weixin_43701894/article/details/132279518
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = None
    del_flag: Optional[int] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime.datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime.datetime] = None

    @field_serializer('create_time')
    def serialize_ct(self, dt: datetime.datetime, _info):
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')

    @field_serializer('update_time')
    def serialize_ut(self, dt: datetime.datetime, _info):
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')


class SysUser(BaseModelWithCommonFields):
    dept_id: Optional[int] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    phonenumber: Optional[str] = None
    sex: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    status: Optional[str] = None
    login_ip: Optional[str] = None
    login_date: Optional[datetime.datetime] = None

    @field_serializer('login_date')
    def serialize_ld(self, dt: datetime.datetime, _info):
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')


class SysConfig(BaseModelWithCommonFields):
    config_name: Optional[str] = None
    remark: Optional[str] = None
    config_key: Optional[str] = None
    config_value: Optional[str] = None
    config_type: Optional[str] = None


class SysDept(BaseModelWithCommonFields):
    parent_id: Optional[int] = None
    ancestors: Optional[str] = None
    dept_name: Optional[str] = None
    order_num: Optional[int] = None
    leader: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None


class SysDictData(BaseModelWithCommonFields):
    dict_type: Optional[str] = None
    dict_label: Optional[str] = None
    dict_value: Optional[str] = None
    order_num: Optional[int] = None
    css_class: Optional[str] = None
    list_class: Optional[str] = None
    as_default: Optional[bool] = None
    status: Optional[str] = None


class SysDictType(BaseModelWithCommonFields):
    dict_name: Optional[str] = None
    dict_type: Optional[str] = None
    remark: Optional[str] = None
    status: Optional[str] = None


class SysMenu(BaseModelWithCommonFields):
    menu_name: Optional[str] = None
    menu_title: Optional[str] = None
    parent_id: Optional[int] = None
    menu_type: Optional[str] = None
    order_num: Optional[int] = None
    path: Optional[str] = None
    component: Optional[str] = None
    query: Optional[str] = None
    affix: Optional[bool] = None
    frame: Optional[bool] = None
    cache: Optional[bool] = None
    full_screen: Optional[bool] = None
    visible: Optional[bool] = None
    status: Optional[str] = None
    perms: Optional[str] = None
    icon: Optional[str] = None
    children: Optional[List['SysMenu']] = None


class SysRole(BaseModelWithCommonFields):
    role_name: Optional[str] = None
    remark: Optional[str] = None
    role_key: Optional[str] = None
    order_num: Optional[int] = None
    status: Optional[str] = None


class SysRoleMenu(BaseModelWithCommonFields):
    menu_id: int = None
    role_id: int = None


class SysRoleUser(BaseModelWithCommonFields):
    user_id: int = None
    role_id: int = None
