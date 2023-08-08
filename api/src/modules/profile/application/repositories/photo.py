from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.core.dtos import BaseDTO
from src.modules.profile.domain.entities.dae.profile_photo import PhotoDAE


class IProfilePhotoRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: PhotoDAE) -> PhotoDAE:
        ...

    @abstractmethod
    async def delete(self, *, entity_id: UUID, profile_id: UUID) -> PhotoDAE:
        ...

    @abstractmethod
    async def get_by_hash(self, *, profile_id: UUID, hash: str) -> PhotoDAE | None:
        ...

    @abstractmethod
    async def photos_count(self, *, profile_id: UUID) -> int:
        ...

    @abstractmethod
    async def get(self, *, entity_id: UUID, profile_id: UUID) -> PhotoDAE:
        ...

    @abstractmethod
    async def fetch(
        self, *, entities_ids: list[UUID], profile_id: UUID
    ) -> list[PhotoDAE]:
        ...

    @abstractmethod
    async def update(self, *, in_entity: PhotoDAE) -> PhotoDAE:
        ...

    @abstractmethod
    async def max_displaying_num(self, *, profile_id: UUID) -> int:
        ...


class IProfilePhotoS3Repository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_dto: BaseDTO) -> None:
        ...

    @abstractmethod
    async def delete(self, *, key: str) -> None:
        ...

    async def drop(self, *, key: str) -> None:
        ...
