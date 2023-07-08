from typing import Annotated

from fastapi import APIRouter, Header
from starlette.status import HTTP_201_CREATED

from src.v1.auth.dtos import (
    InitDataRequestLogin,
    RefreshTokenRequestUpdateTokenPair,
    TokenPairResponse,
)
from src.v1.auth.repositories.refresh_token import RefreshTokenRepository
from src.v1.auth.repositories.user import UserRepository
from src.v1.auth.schemas.refresh_token import (
    RefreshTokenInCreateSchema,
    RefreshTokenInUpdateSchema,
    RefreshTokenOutSchema,
)
from src.v1.auth.schemas.user import UserInCreateSchema, UserOutSchema
from src.v1.auth.usecases.refresh_token import CreateRefreshToken, UpdateRefreshToken
from src.v1.auth.usecases.user import GetOrCreateUser, ReadUser
from src.v1.config.database import DbSession

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "",
    response_model=TokenPairResponse,
    status_code=HTTP_201_CREATED,
)
async def login(
    init_data: InitDataRequestLogin,
    db_session: DbSession,
    user_agent: Annotated[str, Header()],
):
    """
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    user_data = UserInCreateSchema(**init_data.valid_init_data.get("user", {}))
    user: UserOutSchema = await GetOrCreateUser(
        repository=UserRepository(db_session=db_session)
    ).execute(user_data=user_data)

    refresh_token_data = RefreshTokenInCreateSchema(
        user=user.id,
        user_agent=user_agent,
    )
    refresh_token: RefreshTokenOutSchema = await CreateRefreshToken(
        repository=RefreshTokenRepository(db_session=db_session)
    ).execute(refresh_token_data=refresh_token_data)

    return TokenPairResponse(
        access_token=user.access_token,
        refresh_token=refresh_token.value,
    )


@auth_router.put(
    "",
    response_model=TokenPairResponse,
    status_code=HTTP_201_CREATED,
)
async def update_token_pair(
    expired_token: RefreshTokenRequestUpdateTokenPair,
    db_session: DbSession,
    user_agent: Annotated[str, Header()],
):
    """
    Update token pair.

    Returns:
        The new user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's refresh token is invalid
    """

    expired_refresh_token_data = RefreshTokenInUpdateSchema(
        user=expired_token.valid_token_data["user"],
        user_agent=user_agent,
        expired_token=expired_token.value,
    )

    new_refresh_token: RefreshTokenOutSchema = await UpdateRefreshToken(
        repository=RefreshTokenRepository(db_session=db_session)
    ).execute(refresh_token_data=expired_refresh_token_data)

    user: UserOutSchema = await ReadUser(
        repository=UserRepository(db_session=db_session),
    ).execute(user_id=new_refresh_token.user)

    return TokenPairResponse(
        access_token=user.access_token,
        refresh_token=new_refresh_token.value,
    )
