from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

import sentry_sdk
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.ext.asyncio import async_scoped_session
from starlette.requests import Request

from src.v1.auth.views import auth_router
from src.v1.config.database import async_session_factory
from src.v1.config.s3 import S3Session, create_s3_session
from src.v1.config.settings import settings
from src.v1.interest.views import interest_router
from src.v1.photo.views import photo_router
from src.v1.profile.views import profile_router
from src.v1.deck.views import deck_router

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    integrations=[
        SqlalchemyIntegration(),
    ],
)

api = FastAPI()


api.include_router(auth_router, prefix=settings.API_V1_PREFIX, tags=["Auth"])
api.include_router(photo_router, prefix=settings.API_V1_PREFIX, tags=["Photos"])
api.include_router(profile_router, prefix=settings.API_V1_PREFIX, tags=["Profile"])
api.include_router(interest_router, prefix=settings.API_V1_PREFIX, tags=["Interests"])
api.include_router(deck_router, prefix=settings.API_V1_PREFIX, tags=["Deck"])

origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@api.middleware("http")
async def s3_resource_middleware(request: Request, call_next):
    request.state.s3 = create_s3_session()
    response = await call_next(request)
    return response
