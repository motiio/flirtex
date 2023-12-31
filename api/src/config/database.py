from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.requests import Request

from src.config.settings import settings

async_engine = create_async_engine(
    settings.DATABASE_URI,
    pool_size=settings.DATABASE_ENGINE_POOL_SIZE,
    pool_pre_ping=True,
    pool_recycle=300,
    max_overflow=settings.DATABASE_ENGINE_MAX_OVERFLOW,
)


def get_db(request: Request):
    return request.state.db


async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

DbSession = Annotated[AsyncSession, Depends(get_db)]
