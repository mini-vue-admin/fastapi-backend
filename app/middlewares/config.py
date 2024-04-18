from functools import lru_cache
from typing import Union

from pydantic_settings import BaseSettings


# BaseSettings类天然支持从环境变量获取配置。
class Settings(BaseSettings):
    app_name: str = "FastAPI Admin"
    app_author: Union[str, None] = None
    app_author_email: Union[str, None] = None
    app_qps: int = 0

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
