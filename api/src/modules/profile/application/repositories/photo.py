from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.core.dtos import BaseS3DTO
from src.core.types import IN_S3_DTO
from src.modules.profile.domain.entities.dae.profile_photo import PhotoDAE


class IProfilePhotoRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: PhotoDAE) -> PhotoDAE:
        ...

    @abstractmethod
    async def delete(self, *, entity_id: UUID) -> PhotoDAE:
        ...

    @abstractmethod
    async def get_by_hash(self, *, profile_id: UUID, hash: str) -> PhotoDAE | None:
        ...

    @abstractmethod
    async def photos_count(self, *, profile_id: UUID) -> int:
        ...


class IProfilePhotoS3Repository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_dto: IN_S3_DTO) -> None:
        ...

    @abstractmethod
    async def delete(self, *, key: str) -> None:
        ...
