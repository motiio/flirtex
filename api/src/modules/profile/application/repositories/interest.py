from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.profile.domain.entities import Interest


class IInterestRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def fetch(self, *, entities_ids: list[UUID]) -> list[Interest]:
        ...

    @abstractmethod
    async def list(self) -> list[Interest]:
        ...
