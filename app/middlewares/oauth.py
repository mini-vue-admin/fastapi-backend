from datetime import timedelta
from typing import Union, Optional, Set, List

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from constants.base import Status, SystemRoleKey
from models import ResponseData
from models.system.schemas import SysUser
from services.system import user_service, role_service
from utils.encrypt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decrypt_access_token


class WhitelistOAuth2PasswordBearer(OAuth2PasswordBearer):

    def __init__(self, whitelist: Optional[Set[str]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if whitelist is None:
            whitelist = {"/token", "/login", "/healthy", "/info"}
        self.whitelist = whitelist

    async def __call__(self, request: Request) -> Optional[str]:
        # 检查请求的 URL 是否在白名单中
        root_path = request.scope['root_path']
        relative_path = request.url.path[len(root_path):]
        if relative_path in self.whitelist:
            return None
        # 如果不在白名单中，调用父类的 __call__ 方法
        return await super().__call__(request)


oauth2_scheme = WhitelistOAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    if token is None:
        return SysUser.anonymous()
    username = await decrypt_access_token(token)
    user = user_service.get_by_username(username)
    return user


async def get_current_active_user(current_user: SysUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User not exists")
    if current_user.status == Status.DISABLED:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive user")

    roles = role_service.get_by_userid(current_user.id)
    return PrincipleUser(**current_user.__dict__, roles=[i.role_key for i in roles])


class PrincipleUser(SysUser):
    roles: List[str] = []

    def is_admin(self):
        return SystemRoleKey.ADMIN.value in self.roles


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


router = APIRouter()


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=ResponseData[Token])
async def login(form_data: LoginRequest):
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return ResponseData.success(Token(access_token=access_token, token_type="bearer"))
