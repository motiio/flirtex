from uuid import UUID

from src.v1.auth.exceptions import InvalidToken
from src.v1.auth.repositories.refresh_token import RefreshTokenRepository
from src.v1.auth.schemas.refresh_token import (
    RefreshTokenInCreateSchema,
    RefreshTokenInUpdateSchema,
    RefreshTokenOutSchema,
)
from src.v1.base.usecases import BaseUseCase


class CreateRefreshToken(
    BaseUseCase[
        RefreshTokenRepository,
        RefreshTokenInCreateSchema,
        RefreshTokenOutSchema,
    ]
):
    async def execute(self, *, refresh_token_data: RefreshTokenInCreateSchema):
        async with self.repository as repo:
            await self._expire_all_session_tokens(
                user_id=refresh_token_data.user,
                user_agent=refresh_token_data.user_agent,
            )
            refresh_token = await repo.create(in_schema=refresh_token_data)
            return refresh_token

    async def _expire_all_session_tokens(self, *, user_id: UUID, user_agent: str):
        async with self.repository as repo:
            await repo.delete_by_useragent(user_id=user_id, user_agent=user_agent)


class UpdateRefreshToken(
    BaseUseCase[
        RefreshTokenRepository,
        RefreshTokenInUpdateSchema,
        RefreshTokenOutSchema,
    ]
):
    async def execute(
        self,
        *,
        refresh_token_data: RefreshTokenInUpdateSchema,
    ):
        async with self.repository as repo:
            existent_refresh_token = await repo.get_by_value(value=refresh_token_data.expired_token)
            if not existent_refresh_token:
                raise InvalidToken
            await repo.delete(entry_id=existent_refresh_token.id)

            # remove expired_token from input schema to create new token
            del refresh_token_data.expired_token

            new_refresh_token = await repo.create(in_schema=refresh_token_data)
            return RefreshTokenOutSchema.model_validate(new_refresh_token)
