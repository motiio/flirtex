from functools import lru_cache

from pydantic import BaseSettings, Field, PostgresDsn

from src.constants import Environment


class Settings(BaseSettings):
    APP_VERSION: str = "0.1"
    ENVIRONMENT: Environment = Environment.TESTING
    SENTRY_DSN: str | None
    LOG_LEVEL: str = Environment.get_env_log_level

    BOT_TOKEN: str

    DATABASE_URI: PostgresDsn = Field(..., env="DATABASE_URI")
    DATABASE_ENGINE_POOL_SIZE: int = 5
    DATABASE_ENGINE_MAX_OVERFLOW: int = 10

    CORS_ORIGINS: list[str] = ["ALL"]
    CORS_ORIGINS_REGEX: str | None
    CORS_HEADERS: list[str] = [""]

    JWT_SECRET: str
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(..., env="JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int = Field(..., env="JWT_REFRESH_TOKEN_EXPIRE_SECONDS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
