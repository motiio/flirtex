from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

import sentry_sdk
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.ext.asyncio import async_scoped_session
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.auth.routers import auth_router
from src.common.routers import common_router
from src.config.core import config, settings
from src.database.core import async_session_factory
from src.profile.routers import profile_router

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    integrations=[
        SqlalchemyIntegration(),
    ],
)

api = FastAPI(**config)


api.include_router(auth_router, prefix="/auth", tags=["Auth"])
api.include_router(profile_router, prefix="/profile", tags=["Profile"])
api.include_router(common_router, prefix="/common", tags=["Common"])


origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.method == "POST":
            if "content-length" not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
            content_length = int(request.headers["content-length"])
            if content_length > self.max_upload_size:
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        return await call_next(request)


api.add_middleware(LimitUploadSize, max_upload_size=10_000_000)  # ~10MB

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())
    ctx_token = _request_id_ctx_var.set(request_id)
    try:
        db_session = async_scoped_session(
            async_session_factory, scopefunc=get_request_id
        )
        request.state.db = db_session()
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


@api.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@api.get("/user-agent")
async def get_user_agent(user_agent: str = Header(None)):
    """
    Returns:
        The user agent string.
    """
    return {"User-Agent": user_agent}
