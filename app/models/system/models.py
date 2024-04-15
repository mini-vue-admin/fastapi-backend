from sqlalchemy import Column, Integer, String, DateTime

from middlewares.database import Base


# 定义一个包含公共字段的继承基类
class BaseMixin:
    __abstract__ = True  #设置为可继承的基础模型，不创建表

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='ID')
    del_flag = Column(Integer, default=0, comment='删除标志(0代表存在 1代表删除)')
    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=None, comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=None, comment='更新时间')

    # 使这个基类可继承
    __mapper_args__ = {
        'polymorphic_identity': 'base',  # 指定多态标识
        'polymorphic_on': None  # 暂时不指定多态列
    }


class User(Base, BaseMixin):
    __tablename__ = 'sys_user'

    dept_id = Column(Integer, default=None, comment='部门ID')
    username = Column(String(30), nullable=False, comment='用户账号')
    nickname = Column(String(30), nullable=False, comment='用户昵称')
    email = Column(String(50), default=None, comment='用户邮箱')
    phonenumber = Column(String(11), default=None, comment='手机号码')
    sex = Column(String(255), default='2', comment='用户性别（0男 1女 2未知）')
    avatar = Column(String(100), default='', comment='用户头像')
    password = Column(String(100), default='', comment='密码')
    status = Column(String(255), default='0', comment='帐号状态:0正常,1停用')
    login_ip = Column(String(128), default='', comment='最后登录IP')
    login_date = Column(DateTime, default=None, comment='最后登录时间')
