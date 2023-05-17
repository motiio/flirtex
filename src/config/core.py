from pydantic import BaseSettings, Field, PostgresDsn
from fastapi import Depends
from src.constants import Environment
from typing import Annotated
from functools import lru_cache


class Settings(BaseSettings):
    APP_VERSION: str = "0.1"
    ENVIRONMENT: Environment = Environment.LOCAL
    LOG_LEVEL: str = Environment.get_env_log_level

    BOT_TOKEN: str

    DATABASE_URI: PostgresDsn = Field(..., env="DATABASE_URI")
    DATABASE_ENGINE_POOL_SIZE: int = 5
    DATABASE_ENGINE_MAX_OVERFLOW: int = 10

    CORS_ORIGINS: list[str] = ["ALL"]
    CORS_ORIGINS_REGEX: str | None
    CORS_HEADERS: list[str] = [""]

    JWT_SECRET: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(..., env="JWT_REFRESH_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
