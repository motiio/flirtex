from fastapi import Request
from redis import asyncio as aioredis
from starlette.middleware.base import BaseHTTPMiddleware


class RedisMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, redis_pool):
        super().__init__(app)
        self.redis_pool = redis_pool

    async def dispatch(self, request: Request, call_next):
        redis = await aioredis.Redis(connection_pool=self.redis_pool)
        try:
            request.state.redis = redis
            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            await redis.close()
        return response
