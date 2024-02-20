from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository


class IDeckCacheRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def save(self, *, profile_id: UUID, profiles: list[UUID]) -> None: ...

    @abstractmethod
    async def get_batch(self, *, profile_id: UUID, batch_size: int) -> list[UUID]: ...

    @abstractmethod
    async def delete(self, *, profile_id: UUID) -> None: ...
