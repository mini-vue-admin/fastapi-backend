from fastapi import APIRouter

from routers.system import user, menu, config, dict_type, dict_data, dept, role

router = APIRouter()

router.include_router(user.router, prefix="/user")
router.include_router(menu.router, prefix="/menu")
router.include_router(config.router, prefix="/config")
router.include_router(dict_type.router, prefix="/dictType")
router.include_router(dict_data.router, prefix="/dictData")
router.include_router(dept.router, prefix="/dept")
router.include_router(role.router, prefix="/role")
