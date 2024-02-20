from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.deck.domain.entities import Skip


class ISkipRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Skip) -> Skip: ...

    @abstractmethod
    async def get_skip_by_profiles(
        self, *, source_profile: UUID, target_profile: UUID
    ) -> Skip | None: ...

    @abstractmethod
    async def get(self, *, entity_id: UUID) -> Skip | None: ...

    @abstractmethod
    async def delete_by_target(
        self, *, source_profile: UUID, target_profile: UUID
    ) -> Skip | None: ...
