import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from src.config.database import async_session_factory
from src.config.s3 import create_s3_session
from src.config.settings import settings
from src.core.middlewares.db import DatabaseMiddleware
from src.modules.auth.api import auth_router_v1
from src.modules.common.api import common_router_v1
from src.modules.profile.api import profile_router_v1

# from src.v1.deck.views import deck_router
# from src.v1.interest.views import interest_router
# from src.v1.photo.views import photo_router
# from src.v1.profile.views import profile_router

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    integrations=[
        SqlalchemyIntegration(),
    ],
)

api = FastAPI()


api.include_router(auth_router_v1, prefix=settings.API_V1_PREFIX, tags=["Auth"])
api.include_router(profile_router_v1, prefix=settings.API_V1_PREFIX, tags=["Profile"])
api.include_router(common_router_v1, prefix=settings.API_V1_PREFIX, tags=["Common"])

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.add_middleware(
    DatabaseMiddleware,
    session_factory=async_session_factory,
)


@api.middleware("http")
async def s3_resource_middleware(request: Request, call_next):
    request.state.s3 = create_s3_session()
    response = await call_next(request)
    return response
