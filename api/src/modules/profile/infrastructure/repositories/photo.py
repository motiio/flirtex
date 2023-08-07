from typing import Type
from uuid import UUID

from sqlalchemy import func, select

from src.core.repositories.implementations.s3 import BaseS3Repository
from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.profile.application.dtos.photo import PhotoInS3UploadDTO, PhotoOutDTO
from src.modules.profile.application.repositories.photo import (
    IProfilePhotoRepository,
    IProfilePhotoS3Repository,
)
from src.modules.profile.domain.entities.dae.profile_photo import PhotoDAE
from src.modules.profile.infrastructure.models import PhotoORM


class ProfilePhotoRepository(
    BaseSqlAlchemyRepository[
        PhotoDAE,
        PhotoORM,
    ],
    IProfilePhotoRepository,
):
    @property
    def _table(self) -> Type[PhotoORM]:
        return PhotoORM

    @property
    def _entity(self) -> Type[PhotoDAE]:
        return PhotoDAE

    async def get_by_hash(self, *, profile_id: UUID, hash: str) -> PhotoDAE | None:
        q = select(self._table).where(
            self._table.hash == hash, self._table.profile_id == profile_id
        )
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
            return PhotoDAE.create(**result.dict())

        return None

    async def photos_count(self, *, profile_id) -> int:
        q = (
            select(func.count())
            .select_from(self._table)
            .where(self._table.profile_id == profile_id)
        )
        result: int = await self._db_session.scalar(q) or 0
        return result


class ProfilePhotoS3Repository(
    BaseS3Repository[PhotoInS3UploadDTO, PhotoOutDTO], IProfilePhotoS3Repository
):
    @property
    def _bucket_name(self) -> str:
        return "profile-photos"

    @property
    def _out_dto(self) -> Type[PhotoOutDTO]:
        return PhotoOutDTO
