from typing import Type
from uuid import UUID

from sqlalchemy import delete, select

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.auth.application.repositories.refresh_token import (
    IRefreshTokenRepository,
)
from src.modules.auth.domain.entities import RefreshTokenDAE
from src.modules.auth.infrastructure.models import RefreshTokenORM


class RefreshTokenRepository(
    BaseSqlAlchemyRepository[
        RefreshTokenDAE,
        RefreshTokenORM,
    ],
    IRefreshTokenRepository,
):
    @property
    def _table(self) -> Type[RefreshTokenORM]:
        return RefreshTokenORM

    @property
    def _entity(self) -> Type[RefreshTokenDAE]:
        return RefreshTokenDAE

    async def get_by_value(self, *, token_value: UUID) -> RefreshTokenDAE | None:
        q = select(self._table).where(self._table.value == token_value)
        result = (await self._db_session.execute(q)).scalars().first()

        if result:
            return self._entity.create(**result.dict())

        return None

    async def expire_user_tokens(self, *, user: UUID, user_agent: str):
        q = delete(self._table).where(
            self._table.user_agent == user_agent,
            self._table.user == user,
        )
        await self._db_session.execute(q)
