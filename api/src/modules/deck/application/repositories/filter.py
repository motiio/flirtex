from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.deck.domain.entities import Filter


class IFilterRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Filter) -> Filter: ...

    @abstractmethod
    async def update(self, *, in_entity: Filter) -> Filter | None: ...

    @abstractmethod
    async def get_by_profile(self, *, profile_id: UUID) -> Filter | None: ...
