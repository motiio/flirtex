from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository


class IDeckCacheRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def save(self, *, profile_id: UUID, profiles: list[UUID]) -> None:
        ...

    @abstractmethod
    async def get_batch(self, *, profile_id: UUID, batch_size: int) -> list[UUID]:
        ...

    @abstractmethod
    async def get_time_since_creation_s(self, *, profile_id: UUID) -> int | None:
        ...

    @abstractmethod
    async def remove_deck(self, *, profile_id: UUID) -> None:
        ...
