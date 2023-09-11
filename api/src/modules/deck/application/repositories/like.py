from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.deck.domain.entities import Like


class ILikeRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Like) -> Like:
        ...

    @abstractmethod
    async def get_likes_by_profiles(
        self, *, target_profile: UUID, source_profile: UUID
    ) -> tuple[Like | None, Like | None]:
        ...

    @abstractmethod
    async def delete(self, *, entity_id: UUID) -> Like:
        ...

    @abstractmethod
    async def get(self, *, entity_id: UUID) -> Like:
        ...
