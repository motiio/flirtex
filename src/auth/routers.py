from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from src.auth.schemas import (
    UserLoginRequest,
    UserLoginResponse,
)
from src.database.core import DbSession

from .models import User
from .services import (
    create_refresh_token,
    expire_all_refresh_tokens_by_user_agent,
    expire_refresh_token,
    get_or_create_user_by_init_data,
    validate_refresh_token,
)

auth_router = APIRouter()


@auth_router.post("/login", response_model=UserLoginResponse)
async def login_user(
    login_data: UserLoginRequest,
    db_session: DbSession,
    user_agent: Annotated[str, Header()],
):
    user, active_profile = await get_or_create_user_by_init_data(
        db_session=db_session, init_data=login_data.init_data
    )
    await expire_all_refresh_tokens_by_user_agent(
        db_session=db_session, user_id=user.id, user_agent=user_agent
    )

    new_refresh_token = await create_refresh_token(
        db_session=db_session, user_id=user.id, user_agent=user_agent
    )
    if not active_profile:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=[
                {
                    "meta": {
                        "redirect": True,
                        "location": "/profile/register",
                        "access_token": user.access_token,
                        "refresh_token": new_refresh_token.value,
                    },
                    "msg": "User profile not found",
                }
            ],
        )

    return UserLoginResponse(
        access_token=user.access_token,
        refresh_token=new_refresh_token.value,
    )


@auth_router.put("/token/refresh", response_model=UserLoginResponse)
async def refresh_tokens(
    refresh_token: str,
    db_session: DbSession,
    user_agent: Annotated[str, Header()],
) -> UserLoginResponse:
    valid_refresh_token, valid_token_date = await validate_refresh_token(
        db_session=db_session, refresh_token=refresh_token
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
