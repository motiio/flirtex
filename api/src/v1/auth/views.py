from typing import Annotated

from fastapi import APIRouter, Header

from src.v1.auth.dtos import (
    InitDataRequestLogin,
    RefreshTokenRequestUpdateTokenPair,
    TokenPairResponse,
)
from src.v1.auth.repositories.refresh_token import RefreshTokenRepository
from src.v1.auth.repositories.user import UserRepository
from src.v1.auth.schemas.refresh_token import (
    RefreshTokenInCreateSchema,
    RefreshTokenOutSchema,
)
from src.v1.auth.schemas.user import UserInCreateSchema, UserOutSchema
from src.v1.auth.usecases.refresh_token import CreateRefreshToken, UpdateRefreshToken
from src.v1.auth.usecases.user import GetOrCreateUser, ReadUser
from src.v1.config.database import DbSession

auth_router = APIRouter()


@auth_router.post(
    "/auth",
    response_model=TokenPairResponse,
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

    refresh_token_data = RefreshTokenInCreateSchema(user=user.id, user_agent=user_agent)
    refresh_token: RefreshTokenOutSchema = await CreateRefreshToken(
        repository=RefreshTokenRepository(db_session=db_session)
    ).execute(refresh_token_data=refresh_token_data)

    return TokenPairResponse(
        access_token=user.access_token,
        refresh_token=refresh_token.value,
    )


@auth_router.put("/auth", response_model=TokenPairResponse)
async def update_token_pair(
    old_refresh_token: RefreshTokenRequestUpdateTokenPair,
    db_session: DbSession,
    user_agent: Annotated[str, Header()],
):
    """
    Update token pair.

    Returns:
        The new user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's refresh token is invalid
    """

    new_refresh_token_data = RefreshTokenInCreateSchema(
        user=old_refresh_token.valid_token_data["user"],
        user_agent=user_agent,
    )
    new_refresh_token: RefreshTokenOutSchema = await UpdateRefreshToken(
        repository=RefreshTokenRepository(db_session=db_session)
    ).execute(
        refresh_token_data=new_refresh_token_data,
        old_refresh_token_value=old_refresh_token.valid_token_data["value"],
    )

    user: UserOutSchema = await ReadUser(repository=UserRepository(db_session=db_session)).execute(
        user_id=new_refresh_token_data.user
    )

    return TokenPairResponse(
        access_token=user.access_token,
        refresh_token=new_refresh_token.value,
    )
