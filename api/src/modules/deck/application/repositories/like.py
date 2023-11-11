from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.deck.domain.entities import Like
from typing import Optional


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

    @abstractmethod
    async def get_likes_by_target(
        self,
        *,
        target_profile_id: UUID,
        offset: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
    ) -> list[Like]:
        ...
