from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.profile.domain.entities import Profile


class IProfileRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Profile, interests_ids: list[UUID] | None) -> Profile:
        ...

    @abstractmethod
    async def get_by_owner(self, *, owner_id) -> Profile:
        ...

    @abstractmethod
    async def update(self, *, in_entity: Profile, interests_ids: list[UUID] | None) -> Profile:
        ...

    @abstractmethod
    async def delete(self, *, entity_id: UUID) -> None:
        ...
