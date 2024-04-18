from fastapi import APIRouter

from routers.system import user, menu, config

router = APIRouter()

router.include_router(user.router, prefix="/user")
router.include_router(menu.router, prefix="/menu")
router.include_router(config.router, prefix="/config")
