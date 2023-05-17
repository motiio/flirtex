from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from src.config.core import Settings, get_settings


def create_engine(settings: Settings = get_settings()):
    return create_async_engine(
        settings.DATABASE_URI,
        pool_size=settings.DATABASE_ENGINE_POOL_SIZE,
        max_overflow=settings.DATABASE_ENGINE_MAX_OVERFLOW,
    )


def get_db(request: Request):
    return request.state.db


async_session = sessionmaker(create_engine(), expire_on_commit=False, class_=AsyncSession)
DbSession = Annotated[async_session, Depends(get_db)]
