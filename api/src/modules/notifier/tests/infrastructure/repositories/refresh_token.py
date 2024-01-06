from typing import Type
from uuid import UUID

from src.core.repositories.implementations.in_memory import (
    BaseInMemorySqlAlchemnyRepository,
)
from src.modules.auth.application.repositories.refresh_token import (
    IRefreshTokenRepository,
)
from src.modules.auth.domain.entities.dae.refresh_token import RefreshTokenDAE
from src.modules.auth.infrastructure.models import RefreshTokenORM


class RefreshTokenRepository(
    BaseInMemorySqlAlchemnyRepository[
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
        matching_refresh_tokens = filter(
            lambda rt: rt.value == token_value, self._db_session.values()
        )
        refresh_token = next(matching_refresh_tokens, None)

        if refresh_token:
            return self._entity(**refresh_token.dict())

    async def expire_user_tokens(self, *, user: UUID, user_agent: str):
        to_del = [
            key
            for key, refresh_token in self._db_session.items()
            if isinstance(refresh_token, RefreshTokenORM)
            and refresh_token.user == user
            and refresh_token.user_agent == user_agent
        ]
        print(to_del)
        for key in to_del:
            del self._db_session[key]
