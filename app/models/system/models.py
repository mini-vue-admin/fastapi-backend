from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import mapped_column, deferred

from constants.base import DelFlag
from middlewares.database import Base


# 定义一个包含公共字段的继承基类
class BaseMixin:
    __abstract__ = True  # 设置为可继承的基础模型，不创建表

    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='ID')
    del_flag = mapped_column(Integer, default=0, comment='删除标志(0代表存在 1代表删除)',
                             insert_default=DelFlag.UN_DELETE.value)
    create_by = mapped_column(String(64), nullable=True, default='', comment='创建者')
    create_time = mapped_column(DateTime, nullable=True, default=None, comment='创建时间', insert_default=datetime.now)
    update_by = mapped_column(String(64), nullable=True, default='', comment='更新者')
    update_time = mapped_column(DateTime, nullable=True, default=None, comment='更新时间', onupdate=datetime.now)

    # 使这个基类可继承
    __mapper_args__ = {
        'polymorphic_identity': 'base',  # 指定多态标识
        'polymorphic_on': None,  # 暂时不指定多态列
    }


class SysUser(Base, BaseMixin):
    __tablename__ = 'sys_user'

    dept_id = mapped_column(Integer, default=None, comment='部门ID')
    username = mapped_column(String(30), nullable=False, comment='用户账号')
    nickname = mapped_column(String(30), nullable=False, comment='用户昵称')
    email = mapped_column(String(50), default=None, comment='用户邮箱')
    phonenumber = mapped_column(String(11), default=None, comment='手机号码')
    sex = mapped_column(String(255), default='2', comment='用户性别（0男 1女 2未知）')
    avatar = mapped_column(String(100), default='', comment='用户头像')
    password = mapped_column(String(100), default='', comment='密码')
    status = mapped_column(String(255), default='0', comment='帐号状态:0正常,1停用')
    login_ip = mapped_column(String(128), default='', comment='最后登录IP')
    login_date = mapped_column(DateTime, default=None, comment='最后登录时间')


class SysConfig(Base, BaseMixin):
    __tablename__ = 'sys_config'
    config_name = mapped_column(String, default='', comment='参数名称')
    remark = mapped_column(String, default='', comment='备注')
    config_key = mapped_column(String, default='', comment='参数键名')
    config_value = mapped_column(String, default='', comment='参数键值')
    config_type = mapped_column(String(1), default='1', comment='参数类型(0系统内置 1用户定义)')


class SysDept(Base, BaseMixin):
    __tablename__ = 'sys_dept'
    parent_id = mapped_column(Integer, default=0, comment='父部门ID')
    ancestors = mapped_column(String, default='', comment='祖级列表')
    dept_name = mapped_column(String, default='', comment='部门名称')
    order_num = mapped_column(Integer, default=0, comment='显示顺序')
    leader = mapped_column(String, default='', comment='负责人')
    phone = mapped_column(String, default='', comment='联系电话')
    email = mapped_column(String, default='', comment='邮箱')
    status = mapped_column(String(1), default='0', comment='部门状态(0正常 1停用)')


class SysDictData(Base, BaseMixin):
    __tablename__ = 'sys_dict_data'
    dict_type = mapped_column(String, default='', comment='字典类型')
    dict_label = mapped_column(String, default='', comment='字典标签')
    dict_value = mapped_column(String, default='', comment='字典键值')
    order_num = mapped_column(Integer, default=0, comment='字典排序')
    css_class = mapped_column(String, default='', comment='样式属性')
    list_class = mapped_column(String, default='', comment='表格回显样式')
    as_default = mapped_column(Boolean, default=False, comment='是否默认(0否 1是)')
    status = mapped_column(String(1), default='0', comment='状态(0正常 1停用)')


class SysDictType(Base, BaseMixin):
    __tablename__ = 'sys_dict_type'
    dict_name = mapped_column(String, default='', comment='字典名称')
    dict_type = mapped_column(String, default='', comment='字典类型')
    remark = mapped_column(String, default='', comment='备注')
    status = mapped_column(String(1), default='0', comment='字典状态(0正常 1停用)')


class SysMenu(Base, BaseMixin):
    __tablename__ = 'sys_menu'
    menu_name = mapped_column(String, default='', comment='菜单名称')
    menu_title = mapped_column(String, default='', comment='菜单标题')
    parent_id = mapped_column(Integer, default=-1, comment='父菜单ID')
    menu_type = mapped_column(String(1), default='M', comment='菜单类型(M目录 C菜单 F按钮)')
    order_num = mapped_column(Integer, default=0, comment='显示排序')
    path = mapped_column(String, default='', comment='路由地址')
    component = mapped_column(String, default='', comment='组件路径')
    query = mapped_column(String, default='', comment='路由参数')
    affix = mapped_column(Boolean, default=False, comment='是否固定标签(0否 1是)')
    frame = mapped_column(Boolean, default=False, comment='是否外链(0否 1是)')
    cache = mapped_column(Boolean, default=True, comment='是否缓存(0否 1是)')
    full_screen = mapped_column(Boolean, default=True, comment='是否全屏(0否 1是)')
    visible = mapped_column(Boolean, default=True, comment='显示状态(0隐藏 1显示)')
    status = mapped_column(String(1), default='0', comment='菜单状态(0正常 1停用)')
    perms = mapped_column(String, default='', comment='权限标识')
    icon = mapped_column(String, default='#', comment='菜单图标')


class SysRole(Base, BaseMixin):
    __tablename__ = 'sys_role'
    role_name = mapped_column(String, default='', comment='角色名称')
    remark = mapped_column(String, default='', comment='备注')
    role_key = mapped_column(String, default='', comment='角色')
    order_num = mapped_column(Integer, default=0, comment='显示排序')
    status = mapped_column(String(1), default='0', comment='角色状态(0正常 1停用)')


class SysRoleMenu(Base):
    __tablename__ = 'sys_role_menu'
    menu_id = mapped_column(Integer, primary_key=True, )
    role_id = mapped_column(Integer, primary_key=True, )


class SysRoleUser(Base):
    __tablename__ = 'sys_role_user'
    user_id = mapped_column(Integer, primary_key=True, )
    role_id = mapped_column(Integer, primary_key=True, )
