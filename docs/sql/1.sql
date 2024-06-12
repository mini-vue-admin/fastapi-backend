use geeker;

-- ----------------------------
-- 用户表
-- ----------------------------
drop table if exists sys_user;
create table sys_user
(
    id          bigint(20)  not null auto_increment comment 'ID',
    del_flag    tinyint(1)   default '0' comment '删除标志(0代表存在 1代表删除)',
    create_by   varchar(64)  default '' comment '创建者',
    create_time datetime comment '创建时间',
    update_by   varchar(64)  default '' comment '更新者',
    update_time datetime comment '更新时间',
    dept_id     bigint(20)   default null comment '部门ID',
    username    varchar(30) not null comment '用户账号',
    nickname    varchar(30) not null comment '用户昵称',
    email       varchar(50) comment '用户邮箱',
    phonenumber varchar(11) comment '手机号码',
    sex         char(1)      default '2' comment '用户性别(M男 F女 U未知)',
    avatar      varchar(100) default '' comment '用户头像',
    password    varchar(100) default '' comment '密码',
    status      char(1)      default '0' comment '帐号状态(0正常 1停用)',
    login_ip    varchar(128) default '' comment '最后登录IP',
    login_date  datetime comment '最后登录时间',
    primary key (id)
) engine = innodb
  auto_increment = 100 comment = '用户表';

insert into sys_user
values (1, 0, 'admin', sysdate(), null, null, 1, 'admin', '系统管理员', null, null, 'U', null,
        'admin', 0, '127.0.0.1', sysdate());

-- ----------------------------
-- 部门表
-- ----------------------------
drop table if exists sys_dept;
create table sys_dept
(
    id          bigint(20) not null auto_increment comment 'ID',
    del_flag    tinyint(1)  default '0' comment '删除标志(0代表存在 1代表删除)',
    create_by   varchar(64) default '' comment '创建者',
    create_time datetime comment '创建时间',
    update_by   varchar(64) default '' comment '更新者',
    update_time datetime comment '更新时间',
    parent_id   bigint(20)  default 0 comment '父部门id',
    ancestors   varchar(50) default '' comment '祖级列表',
    dept_name   varchar(30) comment '部门名称',
    order_num   int(4)      default 0 comment '显示排序',
    leader      varchar(30) comment '负责人',
    phone       varchar(11) comment '联系电话',
    email       varchar(50) comment '邮箱',
    status      char(1)     default '0' comment '部门状态(0正常 1停用)',
    primary key (id)
) engine = innodb
  auto_increment = 100 comment = '部门表';

insert into sys_dept
values (1, 0, null, sysdate(), null, null, -1, '', '总公司', 0, null, null, null, '0');

-- ----------------------------
-- 角色表
-- ----------------------------
drop table if exists sys_role;
create table sys_role
(
    id          bigint(20)  not null auto_increment comment 'ID',
    del_flag    tinyint(1)  default '0' comment '删除标志(0代表存在 1代表删除)',
    create_by   varchar(64) default '' comment '创建者',
    create_time datetime comment '创建时间',
    update_by   varchar(64) default '' comment '更新者',
    update_time datetime comment '更新时间',
    role_name   varchar(30) not null comment '角色名称',
    remark      varchar(255) comment '备注',
    role_key    varchar(64) not null comment '角色',
    order_num   int(4)      default 0 comment '显示排序',
    status      char(1)     default '0' comment '角色状态(0正常 1停用)',
    primary key (id)
) engine = innodb
  auto_increment = 100 comment = '角色表';

insert into sys_role
values (1, 0, 'admin', sysdate(), null, null, '管理员', '', 'admin', 0, '0');

-- ----------------------------
-- 角色用户表
-- ----------------------------
drop table if exists sys_role_user;
create table sys_role_user
(
    user_id bigint(20) not null comment '用户id',
    role_id bigint(20) not null comment '角色id',
    primary key (user_id, role_id)
) engine = innodb comment = '角色用户表';

insert into sys_role_user
values (1, 1);

-- ----------------------------
-- 菜单表
-- ----------------------------
drop table if exists sys_menu;
create table sys_menu
(
    id          bigint(20)  not null auto_increment comment 'ID',
    del_flag    tinyint(1)   default '0' comment '删除标志(0代表存在 1代表删除)',
    create_by   varchar(64)  default '' comment '创建者',
    create_time datetime comment '创建时间',
    update_by   varchar(64)  default '' comment '更新者',
    update_time datetime comment '更新时间',
    parent_id   bigint(20)  not null comment '父菜单ID',
    menu_title  varchar(50) not null comment '菜单标题',
    menu_name   varchar(50) not null comment '菜单名称',
    menu_type   char(1)      default 'M' comment '菜单类型(M目录 C菜单 F按钮)',
    order_num   int(4)       default 0 comment '显示排序',
    path        varchar(255) default '' comment '路由地址',
    component   varchar(255) comment '组件路径',
    query       varchar(255) comment '路由参数',
    active_menu varchar(255) comment '高亮的菜单',
    affix       tinyint(1)   default 0 comment '是否固定标签(0否 1是)',
    frame       tinyint(1)   default 0 comment '是否外链(0否 1是)',
    cache       tinyint(1)   default 1 comment '是否缓存(0否 1是)',
    full_screen tinyint(1)   default 0 comment '是否全屏(0否 1是)',
    visible     tinyint(1)   default '1' comment '显示状态(0隐藏 1显示)',
    status      char(1)      default '0' comment '菜单状态(0正常 1停用)',
    perms       varchar(100) comment '权限标识',
    icon        varchar(100) default '#' comment '菜单图标',
    primary key (id)
) engine = innodb
  auto_increment = 1000 comment = '菜单表';

insert into sys_menu
values (1, '0', 'admin', sysdate(), null, null, -1, '首页', 'home', 'C', 1, '/home', 'home', null, null, 1, 0, 1, 0, 1,
        '0',
        null, 'HomeFilled'),
       (2, '0', 'admin', sysdate(), null, null, -1, '系统管理', 'system', 'M', 999, '/system', null, null, null, 0, 0,
        1, 0,
        1,
        '0',
        null, 'Tools'),
       (3, '0', 'admin', sysdate(), null, null, 2, '用户管理', 'user', 'C', 1, '/system/user', 'system/user', null,
        null, 0, 0,
        1, 0, 1,
        '0',
        null, 'UserFilled'),
       (4, '0', 'admin', sysdate(), null, null, 2, '角色管理', 'role', 'C', 2, '/system/role', 'system/role', null,
        null, 0, 0,
        1, 0, 1,
        '0',
        null, 'Avatar'),
       (5, '0', 'admin', sysdate(), null, null, 2, '部门管理', 'dept', 'C', 3, '/system/dept', 'system/dept', null,
        null, 0, 0,
        1, 0, 1,
        '0',
        null, 'Stamp'),
       (6, '0', 'admin', sysdate(), null, null, 2, '菜单管理', 'menu', 'C', 4, '/system/menu', 'system/menu', null,
        null, 0, 0,
        1, 0, 1,
        '0',
        null, 'Menu'),
       (7, '0', 'admin', sysdate(), null, null, 2, '字典管理', 'dictType', 'C', 5, '/system/dict-type',
        'system/dictType', null,
        null, 0, 0,
        1, 0, 1,
        '0',
        null, 'Management'),
       (8, '0', 'admin', sysdate(), null, null, 2, '参数配置', 'config', 'C', 6, '/system/config', 'system/config',
        null, null, 0,
        0, 1, 0, 1,
        '0',
        null, 'List');


-- ----------------------------
-- 角色才菜单表
-- ----------------------------
drop table if exists sys_role_menu;
create table sys_role_menu
(
    menu_id bigint(20) not null comment '菜单id',
    role_id bigint(20) not null comment '角色id',
    primary key (menu_id, role_id)
) engine = innodb comment = '角色菜单表';
INSERT INTO sys_role_menu (menu_id, role_id)
VALUES (1, 1),
       (2, 1),
       (3, 1),
       (4, 1),
       (5, 1),
       (6, 1),
       (7, 1),
       (8, 1);


-- ----------------------------
-- 字典类型表
-- ----------------------------
drop table if exists sys_dict_type;
create table sys_dict_type
(
    id          bigint(20) not null auto_increment comment 'ID',
    del_flag    tinyint(1)   default '0' comment '删除标志(0代表存在 1代表删除)',
    create_by   varchar(64)  default '' comment '创建者',
    create_time datetime comment '创建时间',
    update_by   varchar(64)  default '' comment '更新者',
    update_time datetime comment '更新时间',
    dict_name   varchar(100) default '' comment '字典名称',
    dict_type   varchar(100) default '' comment '字典类型',
    remark      varchar(255) comment '备注',
    status      char(1)      default '0' comment '字典状态(0正常 1停用)',
    primary key (id)
) engine = innodb
  auto_increment = 100 comment = '字典类型表';

insert into sys_dict_type
values (1, '0', 'admin', sysdate(), null, null, '状态', 'common.status', '通用状态字典', '0'),
       (2, '0', 'admin', sysdate(), null, null, '配置类型', 'system.config.type', '系统配置类型', '0'),
       (3, '0', 'admin', sysdate(), null, null, '菜单类型', 'system.menu.type', '系统菜单类型', '0'),
       (4, '0', 'admin', sysdate(), null, null, '用户性别', 'system.user.sex', '系统用户性别', '0');

-- ----------------------------
-- 字典数据表
-- ----------------------------
drop table if exists sys_dict_data;
create table sys_dict_data
(
    id          bigint(20) not null auto_increment comment 'ID',
    del_flag    tinyint(1)   default '0' comment '删除标志(0代表存在 1代表删除)',
    create_by   varchar(64)  default '' comment '创建者',
    create_time datetime comment '创建时间',
    update_by   varchar(64)  default '' comment '更新者',
    update_time datetime comment '更新时间',
    dict_type   varchar(100) default '' comment '字典类型',
    dict_label  varchar(100) default '' comment '字典标签',
    dict_value  varchar(100) default '' comment '字典键值',
    order_num   int(4)       default 0 comment '字典排序',
    css_class   varchar(100) comment '样式属性',
    list_class  varchar(100) comment '表格回显样式',
    as_default  tinyint(1)   default 0 comment '是否默认(0否 1是)',
    status      char(1)      default '0' comment '状态(0正常 1停用)',
    primary key (id)
) engine = innodb
  auto_increment = 1000 comment = '字典数据表';

insert into sys_dict_data
values (1, '0', 'admin', sysdate(), null, null, 'common.status', '正常', '0', 0, 'primary', null, 0, '0'),
       (2, '0', 'admin', sysdate(), null, null, 'common.status', '停用', '1', 1, 'danger', null, 0, '0'),
       (3, '0', 'admin', sysdate(), null, null, 'system.config.type', '系统配置', '0', 0, 'primary', null, 0, '0'),
       (4, '0', 'admin', sysdate(), null, null, 'system.config.type', '用户配置', '1', 1, 'primary', null, 0, '0'),
       (5, '0', 'admin', sysdate(), null, null, 'system.menu.type', '目录', 'M', 0, 'warning', null, 0, '0'),
       (6, '0', 'admin', sysdate(), null, null, 'system.menu.type', '菜单', 'C', 1, 'primary', null, 0, '0'),
       (7, '0', 'admin', sysdate(), null, null, 'system.menu.type', '按钮', 'F', 2, 'success', null, 0, '0'),
       (8, '0', 'admin', sysdate(), null, null, 'system.user.sex', '未知', 'U', 2, 'primary', null, 0, '0'),
       (9, '0', 'admin', sysdate(), null, null, 'system.user.sex', '男', 'M', 2, 'primary', null, 0, '0'),
       (10, '0', 'admin', sysdate(), null, null, 'system.user.sex', '女', 'F', 2, 'primary', null, 0, '0');

-- ----------------------------
-- 参数配置表
-- ----------------------------
drop table if exists sys_config;
create table sys_config
(
    id           bigint(20) not null auto_increment comment 'ID',
    del_flag     tinyint(1)   default '0' comment '删除标志(0代表存在 1代表删除)',
    create_by    varchar(64)  default '' comment '创建者',
    create_time  datetime comment '创建时间',
    update_by    varchar(64)  default '' comment '更新者',
    update_time  datetime comment '更新时间',
    config_name  varchar(100) default '' comment '参数名称',
    remark       varchar(255) comment '备注',
    config_key   varchar(100) default '' comment '参数键名',
    config_value varchar(500) default '' comment '参数键值',
    config_type  char(1)      default '1' comment '参数类型(0系统内置 1用户定义)',
    primary key (id)
) engine = innodb
  auto_increment = 100 comment = '参数配置表';
insert into sys_config
values (1, '0', 'admin', sysdate(), null, null, '用户初始密码', '', 'system.user.initPassword', '123456', '0');