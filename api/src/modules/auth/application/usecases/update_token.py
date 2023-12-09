from config.settings import settings
from core.usecases import IUseCase
from auth.application.dtos import (
    UpdateTokenInDTO,
    UpdateTokenOutDTO,
)
from auth.application.repositories import (
    IRefreshTokenRepository,
    IUserRepository,
)
from auth.application.utils.jwt import generate_token
from auth.domain.entities import RefreshTokenDAE
from auth.domain.entities.de.user import User
from auth.domain.exceptions import InvalidJWTToken, UserNotFound


class UpdateTokenUsecase(IUseCase):
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        refresh_token_repository: IRefreshTokenRepository,
    ):
        self._user_repo: IUserRepository = user_repository
        self._refresh_token_repo: IRefreshTokenRepository = refresh_token_repository

    async def execute(self, in_dto: UpdateTokenInDTO) -> UpdateTokenOutDTO:
        async with self._user_repo, self._refresh_token_repo:
            existent_user: User | None = await self._user_repo.get(entity_id=in_dto.user)
            if not existent_user:
                raise UserNotFound

            existent_refresh_token = await self._refresh_token_repo.get_by_value(
                token_value=in_dto.value,
            )
            if not existent_refresh_token:
                raise InvalidJWTToken

            await self._refresh_token_repo.expire_user_tokens(
                user=existent_user.id, user_agent=in_dto.user_agent
            )

            new_refresh_token_dae = RefreshTokenDAE.create(
                **in_dto.model_dump(exclude={"value"}),
                value=generate_token(
                    sub=str(existent_user.id),  # type: ignore
                    expiration_seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
                ),
            )

            new_refresh_token = await self._refresh_token_repo.create(
                in_entity=new_refresh_token_dae
            )

            return UpdateTokenOutDTO(
                access_token=generate_token(
                    sub=str(existent_user.id),  # type: ignore
                    expiration_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
                    secret=settings.JWT_SECRET,
                ),
                refresh_token=new_refresh_token.value,
            )
