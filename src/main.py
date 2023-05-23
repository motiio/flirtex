from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

import sentry_sdk
from fastapi import FastAPI
from pydantic import BaseModel
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.orm import scoped_session
from starlette.requests import Request

from src.auth.routers import auth_router
from src.common.routers import common_router
from src.config.core import settings
from src.profile.routers import profile_router

from .database.core import async_session

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    integrations=[
        SqlalchemyIntegration(),
    ],
)

api = FastAPI(
    title="API",
    description="",
)

api.include_router(auth_router, prefix="/auth", tags=["Auth"])
api.include_router(profile_router, prefix="/profile", tags=["Profile"])
api.include_router(common_router, prefix="/common", tags=["Common"])

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())
    ctx_token = _request_id_ctx_var.set(request_id)
    try:
        session = scoped_session(async_session, scopefunc=get_request_id)
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        await request.state.db.close()
    _request_id_ctx_var.reset(ctx_token)
    return response


class Item(BaseModel):
    name: str


@api.get("/sentry-debug")
async def trigger_error():
    pass


@api.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
