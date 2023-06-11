from calendar import week
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from src.auth.schemas import (
    UserLoginRequest,
    UserLoginResponse,
)
from src.database.core import DbSession
from src.profile.models import Profile

from .models import User
from .services import (
    create_refresh_token,
    expire_all_refresh_tokens_by_user_agent,
    expire_refresh_token,
    get_or_create_user_by_init_data,
    validate_refresh_token,
)

auth_router = APIRouter()


@auth_router.post("")
async def login_user(
    login_data: UserLoginRequest,
    db_session: DbSession,
    user_agent: Annotated[str, Header()],
):
    """
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    user: User = await get_or_create_user_by_init_data(
        db_session=db_session, init_data=login_data.init_data
    )
    await expire_all_refresh_tokens_by_user_agent(
        db_session=db_session,
        user_id=user.id,
        user_agent=user_agent,
    )

    new_refresh_token = await create_refresh_token(
        db_session=db_session, user_id=user.id, user_agent=user_agent
    )

    return UserLoginResponse(
        access_token=user.access_token,
        refresh_token=new_refresh_token.value,
    )


@auth_router.put("", response_model=UserLoginResponse)
async def refresh_tokens(
    refresh_token: str,
    db_session: DbSession,
    user_agent: Annotated[str, Header()],
) -> UserLoginResponse:
    valid_refresh_token, valid_token_date = await validate_refresh_token(
        db_session=db_session, refresh_token=refresh_token
    )
    if not valid_refresh_token or not valid_token_date:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=[{"msg": "Invalid token signature"}],
        )
    user = User(id=int(valid_token_date.get("sub")))
    await expire_refresh_token(db_session=db_session, refresh_token_value=refresh_token)
    new_refresh_token = await create_refresh_token(
        db_session=db_session, user_id=user.id, user_agent=user_agent
    )
    return UserLoginResponse(
        access_token=user.access_token,
        refresh_token=new_refresh_token.value,
    )
