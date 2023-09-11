from redis import asyncio as aioredis
from redis.asyncio.client import Pipeline

from src.core.aio import IAsyncContextManagerRepository


class BaseRedisRepository(IAsyncContextManagerRepository):
    def __init__(
        self,
        *,
        session: aioredis.Redis,
    ):
        self._session = session
        self._pepiline: Pipeline

    async def commit(self):
        await self._pepiline.execute()

    async def rollback(self):
        await self._pepiline.reset()

    async def __aenter__(self):
        self._pepiline = await self._session.pipeline()
        return self._pepiline

    async def __aexit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            # TODO добавить логирование
            await self.rollback()
        await self.commit()
