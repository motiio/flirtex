import os
from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class EnvironmentEnum(str, Enum):
    PRODUCTION = "production"
    LOCAL = "local"


class GlobalConfig(BaseSettings):
    TITLE: str = "API"
    APP_VERSION: str = "0.1"
    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    API_V1_PREFIX: str = "/v1"

    SENTRY_DSN: str | None

    BOT_TOKEN: str

    DATABASE_URI: str
    DATABASE_ENGINE_POOL_SIZE: int = 5
    DATABASE_ENGINE_MAX_OVERFLOW: int = 10

    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_PROFILES_BUCKET_NAME: str
    S3_CLOUD_ENDPOINT: str = "https://storage.yandexcloud.net"

    JWT_SECRET: str
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int

    MAX_PROFILE_PHOTO_SIZE_B: int
    MAX_PROFILE_PHOTOS_COUNT: int = 7

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        env_file_encoding = "utf-8"


class LocalConfig(GlobalConfig):
    """Local configurations."""

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL


class ProdConfig(GlobalConfig):
    """Production configurations."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        if self.environment == EnvironmentEnum.PRODUCTION.value:
            return ProdConfig()  # type: ignore
        return LocalConfig()  # type: ignore


@lru_cache()
def get_configuration() -> GlobalConfig:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
