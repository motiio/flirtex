from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.modules.profile.domain.entities import Profile


class IProfileRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Profile) -> Profile:
        ...

    @abstractmethod
    async def get_by_owner(self, *, owner_id) -> Profile:
        ...

    @abstractmethod
    async def update(self, *, in_entity: Profile, interests_ids: list[UUID] | None) -> Profile:
        ...

    @abstractmethod
    async def delete(self, *, entity_id: UUID) -> Profile:
        ...

    @abstractmethod
    async def get(self, *, entity_id: UUID) -> Profile | None:
        ...

    @abstractmethod
    async def fetch(self, *, entities_ids: list[UUID], ordering: bool = False) -> list[Profile]:
        ...
