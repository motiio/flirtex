from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.orm import scoped_session
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routers import auth_router
from src.common.routers import common_router
from src.config.core import settings
from src.profile.routers import profile_router
from src.s3.core import S3Client, s3_session

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

origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())
    ctx_token = _request_id_ctx_var.set(request_id)
    async with s3_session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    ) as s3_client:
        try:
            db_session = scoped_session(async_session, scopefunc=get_request_id)
            request.state.db = db_session()
            request.state.s3_client = s3_client

            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            await request.state.db.close()
        _request_id_ctx_var.reset(ctx_token)
    return response


@api.get("/sentry-debug")
async def trigger_error():
    pass


@api.get("/s3", response_model=None)
async def check_s3(s3_session: S3Client):
    s3_session.put_object(Bucket="user4", Body="", Key="test-folder/")
    for key in s3_session.list_objects(Bucket="user4")["Contents"]:
        return key["Key"]


@api.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
