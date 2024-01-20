from typing import Annotated

from fastapi import Depends
from redis import asyncio as aioredis

from src.config.settings import settings


def _create_redis_pool():
    return aioredis.ConnectionPool.from_url(
        url=settings.REDIS_HOST.unicode_string(), port=6379, db=0, decode_responses=True
    )


redis_pool = _create_redis_pool()


async def get_redis_db():
    try:
        redis = await aioredis.Redis(connection_pool=redis_pool)
        yield redis
    except Exception as e:
        raise e from None
    finally:
        await redis.close()


RedisSession = Annotated[aioredis.Redis, Depends(get_redis_db)]

