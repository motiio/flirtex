from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository


class IDeckRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def generate(self, *, profile_id: UUID) -> list[UUID]: ...
