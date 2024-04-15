from functools import lru_cache
from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Admin"
    app_author: Union[str, None] = None
    app_author_email: Union[str, None] = None
    app_qps: int = 50

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
