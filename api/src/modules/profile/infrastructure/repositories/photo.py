from typing import Type
from uuid import UUID

from sqlalchemy import delete, func, select

from src.core.repositories.implementations.s3 import BaseS3Repository
from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.profile.application.dtos.photo import PhotoInS3UploadDTO, PhotoOutDTO
from src.modules.profile.application.repositories.photo import (
    IProfilePhotoRepository,
    IProfilePhotoS3Repository,
)
from src.modules.profile.domain.entities import ProfilePhoto
from src.modules.profile.infrastructure.models import PhotoORM


class ProfilePhotoRepository(
    BaseSqlAlchemyRepository[
        ProfilePhoto,
        PhotoORM,
    ],
    IProfilePhotoRepository,
):
    @property
    def _table(self) -> Type[PhotoORM]:
        return PhotoORM

    @property
    def _entity(self) -> Type[ProfilePhoto]:
        return ProfilePhoto

    async def get_by_hash(self, *, profile_id: UUID, hash: str) -> ProfilePhoto | None:
        q = select(self._table).where(
            self._table.hash == hash, self._table.profile_id == profile_id
        )
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
            return self._entity.create(**result.dict())

        return None

    async def delete(self, *, entity_id: UUID, profile_id: UUID) -> ProfilePhoto:
        q = (
            delete(self._table)
            .where(self._table.id == entity_id, self._table.profile_id == profile_id)
            .returning(self._table)
        )
        result = (await self._db_session.execute(q)).scalars().one()
        return self._entity.create(**result.dict())

    async def get(self, *, entity_id: UUID, profile_id: UUID) -> ProfilePhoto | None:
        q = select(self._table).where(
            self._table.id == entity_id, self._table.profile_id == profile_id
        )
        result = (await self._db_session.execute(q)).scalars().first()

        if result:
            return self._entity.create(**result.dict())

        return None

    async def max_displaying_num(self, *, profile_id: UUID) -> int:
        q = (
            select(func.max(self._table.displaying_order))
            .select_from(self._table)
            .where(self._table.profile_id == profile_id)
        )
        result: int = await self._db_session.scalar(q) or 0
        return result

    async def photos_count(self, *, profile_id) -> int:
        q = (
            select(func.count())
            .select_from(self._table)
            .where(self._table.profile_id == profile_id)
        )
        result: int = await self._db_session.scalar(q) or 0
        return result

    async def fetch(self, *, entities_ids: list[UUID], profile_id) -> list[ProfilePhoto]:  # type: ignore
        q = select(self._table).where(
            self._table.id.in_(entities_ids), self._table.profile_id == profile_id
        )
        entries = (await self._db_session.execute(q)).scalars().all()
        return [self._entity.create(**entry.dict()) for entry in entries]


class ProfilePhotoS3Repository(
    BaseS3Repository[PhotoInS3UploadDTO, PhotoOutDTO], IProfilePhotoS3Repository
):
    @property
    def _bucket_name(self) -> str:
        return "profile-photos"

    @property
    def _out_dto(self) -> Type[PhotoOutDTO]:
        return PhotoOutDTO
