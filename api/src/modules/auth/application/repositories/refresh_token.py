from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.auth.domain.entities.dae.refresh_token import RefreshTokenDAE


class IRefreshTokenRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def get_by_value(self, *, token_value: str) -> RefreshTokenDAE | None:
        ...

    @abstractmethod
    async def expire_user_tokens(self, *, user: UUID, user_agent: str) -> None:
        ...
