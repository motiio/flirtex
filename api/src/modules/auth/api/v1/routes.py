from typing import Annotated, Any

from auth.api.v1.schemas import (
    TelegramLoginRequestSchema,
    UpdateTokenRequestSchema,
)
from auth.api.v1.schemas.out import (
    TelegramLoginOutSchema,
    UpdateTokenOutSchema,
)
from auth.application.dependencies import (
    TelegramLoginService,
    UpdateTokenService,
)
from auth.application.dtos import (
    TelegramLoginInDTO,
    TelegramLoginOutDTO,
    UpdateTokenInDTO,
    UpdateTokenOutDTO,
)
from fastapi import APIRouter, Header
from starlette.status import HTTP_201_CREATED

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "",
    response_model=TelegramLoginOutSchema,
    status_code=HTTP_201_CREATED,
)
async def login(
    login_data: TelegramLoginRequestSchema,
    login_service: TelegramLoginService,
    user_agent: Annotated[str, Header()],
) -> dict[str, Any]:
    """
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    credentials: TelegramLoginOutDTO = await login_service.execute(
        in_dto=TelegramLoginInDTO(
            **login_data.model_dump(),
            user_agent=user_agent,
        )
    )
    return credentials.model_dump()


@auth_router.put(
    "",
    response_model=UpdateTokenOutSchema,
    status_code=HTTP_201_CREATED,
)
async def update_token_pair(
    update_token_data: UpdateTokenRequestSchema,
    update_token_service: UpdateTokenService,
    user_agent: Annotated[str, Header()],
) -> dict[str, Any]:
    credentials: UpdateTokenOutDTO = await update_token_service.execute(
        in_dto=UpdateTokenInDTO(
            **update_token_data.model_dump(),
            user_agent=user_agent,
        )
    )
    return credentials.model_dump()
