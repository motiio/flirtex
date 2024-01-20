from functools import partial
from typing import Annotated

from fastapi import Depends
from pydantic import RedisDsn
from redis import asyncio as aioredis

from src.config.settings import settings


def create_redis_pool(*, redis_url: RedisDsn):
    conn = aioredis.ConnectionPool.from_url(
        url=redis_url.unicode_string(),
    )
    return conn

redis_deck_pool = create_redis_pool(redis_url=settings.REDIS_DECK_URL)
redis_notifier_pool = create_redis_pool(redis_url=settings.REDIS_NOTIFIER_URL)

async def get_redis_connection(pool: aioredis.ConnectionPool):
    try:
        redis = await aioredis.Redis(connection_pool=pool)
        yield redis
    except Exception as e:
        raise e from None
    finally:
        await redis.close()

get_deck_connection = partial(get_redis_connection, redis_deck_pool)
get_notifier_connection = partial(get_redis_connection, redis_notifier_pool)

DeckRedisSession = Annotated[aioredis.Redis, Depends(get_deck_connection)]
RedisNotifierSession = Annotated[aioredis.Redis, Depends(get_notifier_connection)]
