from typing import Optional, cast

from pydantic import Field

from config.settings import settings
from core.dtos import BaseDTO
from core.usecases import IUseCase
from auth.application.dtos import (
    TelegramLoginInDTO,
    TelegramLoginOutDTO,
)
from auth.application.repositories import (
    IRefreshTokenRepository,
    IUserRepository,
)
from auth.application.utils.jwt import generate_token
from auth.domain.entities import RefreshTokenDAE, User


class _TelegramUserInfo(BaseDTO):
    tg_id: int = Field(alias="id")
    tg_username: Optional[str] = Field(alias="username")
    tg_first_name: Optional[str] = Field(alias="first_name")
    tg_last_name: Optional[str] = Field(None, alias="last_name")
    tg_is_premium: Optional[bool] = Field(None, alias="is_premium")
    tg_language_code: Optional[str] = Field(None, alias="language_code")


class TelegramLoginUsecase(IUseCase):
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        refresh_token_repository: IRefreshTokenRepository,
    ):
        self._user_repo: IUserRepository = user_repository
        self._refresh_token_repo: IRefreshTokenRepository = refresh_token_repository

    async def execute(self, in_dto: TelegramLoginInDTO) -> TelegramLoginOutDTO:
        tg_user_info: _TelegramUserInfo = _TelegramUserInfo(
            **cast(dict, in_dto.tg_login_data.get("user"))
        )
        async with self._user_repo, self._refresh_token_repo:
            user = await self._user_repo.get_by_tg_id(tg_id=tg_user_info.tg_id)
            if not user:
                user = User.create(**tg_user_info.model_dump())
                await self._user_repo.create(in_entity=user)

            await self._refresh_token_repo.expire_user_tokens(
                user=user.id, user_agent=in_dto.user_agent
            )
            new_refresh_token = RefreshTokenDAE.create(
                user=user.id,
                user_agent=in_dto.user_agent,
                value=generate_token(
                    sub=str(user.id),
                    expiration_seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
                    secret=settings.JWT_SECRET,
                ),
            )
            await self._refresh_token_repo.create(in_entity=new_refresh_token)

        return TelegramLoginOutDTO(
            access_token=generate_token(
                sub=str(user.id),
                expiration_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
                secret=settings.JWT_SECRET,
            ),
            refresh_token=new_refresh_token.value,
        )
