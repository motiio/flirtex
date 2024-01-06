from typing import Annotated

from fastapi import Depends
from redis import asyncio as aioredis
from starlette.requests import Request

from src.config.settings import settings


def create_redis_pool():
    return aioredis.ConnectionPool.from_url(
        url=settings.REDIS_HOST, port=6379, db=0, decode_responses=True
    )


async def get_deck_redis(request: Request):
    await request.state.redis.select(settings.DECK_REDIS_DB)
    return request.state.redis


DeckRedisSession = Annotated[aioredis.Redis, Depends(get_deck_redis)]
