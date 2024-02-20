from aiogram.utils.web_app import WebAppInitData, WebAppUser

from src.config.settings import settings
from src.core.usecases import IUseCase
from src.modules.auth.application.dtos import (
    TelegramLoginInDTO,
    TelegramLoginOutDTO,
)
from src.modules.auth.application.repositories import (
    IRefreshTokenRepository,
    IUserRepository,
)
from src.modules.auth.application.utils.jwt import generate_token
from src.modules.auth.domain.entities import RefreshTokenDAE, User
from src.modules.auth.domain.exceptions import InitDataUserNotFound


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
        web_app_init_data: WebAppInitData = in_dto.web_app_init_data
        tg_user: WebAppUser | None = web_app_init_data.user
        if not tg_user:
            raise InitDataUserNotFound

        async with self._user_repo, self._refresh_token_repo:
            user = await self._user_repo.get_by_tg_id(tg_id=tg_user.id)
            if not user:
                user = User.create(
                    tg_id=tg_user.id,
                    tg_username=tg_user.username,
                    tg_last_name=tg_user.last_name,
                    tg_first_name=tg_user.first_name,
                    tg_language_code=tg_user.language_code,
                    tg_is_premium=False,
                )
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
