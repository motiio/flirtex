from uuid import UUID

from src.v1.auth.exceptions import InvalidToken
from src.v1.auth.repositories.refresh_token import RefreshTokenRepository
from src.v1.auth.schemas.refresh_token import (
    RefreshTokenInCreateSchema,
    RefreshTokenOutSchema,
)
from src.v1.config.usecases import BaseUseCase


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
        RefreshTokenInCreateSchema,
        RefreshTokenOutSchema,
    ]
):
    async def execute(
        self, *, refresh_token_data: RefreshTokenInCreateSchema, old_refresh_token_value: str
    ):
        async with self.repository as repo:
            existent_refresh_token = await repo.get_by_value(value=old_refresh_token_value)
            if not existent_refresh_token:
                raise InvalidToken
            await repo.delete(entry_id=existent_refresh_token.id)
            new_refresh_token = await repo.create(in_schema=refresh_token_data)
            return new_refresh_token
