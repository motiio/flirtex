from typing import Type
from uuid import UUID

from sqlalchemy import delete, select

from src.v1.auth.models import RefreshToken
from src.v1.auth.schemas.refresh_token import (
    RefreshTokenInCreateSchema,
    RefreshTokenInUpdateSchema,
)
from src.v1.base.repositories.db import (
    BaseReadOnlyRepository,
    BaseWriteOnlyRepository,
)


class RefreshTokenRepository(
    BaseReadOnlyRepository[RefreshToken],
    BaseWriteOnlyRepository[
        RefreshTokenInCreateSchema,
        RefreshTokenInUpdateSchema,
        RefreshToken,
    ],
):
    @property
    def _table(self) -> Type[RefreshToken]:
        return RefreshToken

    async def delete_by_useragent(
        self,
        *,
        user_id: UUID,
        user_agent: str,
    ) -> None:
        q = delete(self._table).where(
            self._table.user_agent == user_agent,
            self._table.user == user_id,
        )
        await self._db_session.execute(q)

    async def get_by_value(
        self,
        *,
        value: str,
    ):
        q = select(self._table).where(self._table.value == value)
        return (await self._db_session.execute(q)).scalars().first()
