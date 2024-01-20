import os
from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import AliasChoices, BaseModel, Field, RedisDsn
from pydantic_settings import BaseSettings


class EnvironmentEnum(str, Enum):
    PRODUCTION = "production"
    LOCAL = "local"


class SubModel(BaseModel):
    foo: str = "bar"
    apple: int = 1


class GlobalConfig(BaseSettings):
    APP_VERSION: str = "0.1"
    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    API_V1_PREFIX: str = "/v1"

    JWT_SECRET: str

    REDIS_HOST: RedisDsn = Field(validation_alias=AliasChoices("REDIS_HOST", "REDIS_URL"))
    NOTIFIER_REDIS_DB: int = Field(
        validation_alias=AliasChoices("NOTIFIER_REDIS_DB", "REDIS_DB")
    )
    STREAM_TTL_S: int = Field(
        1_209_600, validation_alias=AliasChoices("NOTIFIER_REDIS_DB", "REDIS_DB")
    )

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
