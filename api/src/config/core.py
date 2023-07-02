import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "0.1"
    ENVIRONMENT: str = "DEV"
    SENTRY_DSN: str | None
    # LOG_LEVEL: str = Environment.get_env_log_level

    BOT_TOKEN: str

    DATABASE_URI: str
    DATABASE_ENGINE_POOL_SIZE: int = 5
    DATABASE_ENGINE_MAX_OVERFLOW: int = 10

    CORS_ORIGINS: list[str] = ["ALL"]
    CORS_HEADERS: list[str] = [""]

    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_PROFILES_BUCKET_NAME: str
    S3_CLOUD_ENDPOINT: str = "https://storage.yandexcloud.net"

    JWT_SECRET: str
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int

    MAX_PROFILE_PHOTO_SIZE_B: int
    MAX_PROFILE_PHOTOS_COUNT: int = 7

    SHORT_URL_RESOURCE: str = "https://clck.ru/--"

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    settings = Settings()
    print(settings)
    return settings


settings = get_settings()

config: dict = {
    "title": "API",
}
