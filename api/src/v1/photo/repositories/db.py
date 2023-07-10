from collections.abc import Sequence
from sqlalchemy import func, select, delete, update
from src.v1.photo.models import Photo
from src.v1.base.repositories.db import (
    BaseReadOnlyRepository,
    BaseWriteOnlyRepository,
)
from src.v1.photo.schemas import (
    PhotoInCreateSchema,
    PhotoInUpdateSchema,
)
from typing import Optional, Type
from uuid import UUID


class PhotoRepository(
    BaseReadOnlyRepository[Photo],
    BaseWriteOnlyRepository[
        PhotoInCreateSchema,
        PhotoInUpdateSchema,
        Photo,
    ],
):
    @property
    def _table(self) -> Type[Photo]:
        return Photo

    async def get_profile_photo_count(self, profile_id: UUID) -> int:
        q = (
            select(func.count())
            .select_from(self._table)
            .where(self._table.profile_id == profile_id)
        )
        result: int = await self._db_session.scalar(q) or 0
        return result

    async def get_profile_photos(self, *, profile_id: UUID) -> Sequence[Photo]:
        q = select(self._table).where(self._table.profile_id == profile_id)
        result = (await self._db_session.execute(q)).scalars().all()
        return result

    async def get_profile_photo_by_hash(self, *, profile_id: UUID, hash: str):
        q = select(self._table).where(
            self._table.profile_id == profile_id, self._table.hash == hash
        )
        result = (await self._db_session.execute(q)).scalars().first()
        return result

    async def delete(self, *, photo_id: UUID, profile_id: UUID):
        q = (
            delete(self._table)
            .where(
                self._table.id == photo_id,
                self._table.profile_id == profile_id,
            )
            .returning(self._table)
        )
        entry = (await self._db_session.execute(q)).scalars().first()
        return entry

    async def set_short_url(self, *, photo_id, short_url, presigned_url):
        q = (
            update(self._table)
            .where(self._table.id == photo_id)
            .values(
                presigned_url=presigned_url,
                short_url=short_url,
            )
        )
        await self._db_session.execute(q)

    async def get_redirect_by_short_url(self, *, short_url: str) -> Optional[str]:
        q = select(self._table.presigned_url).where(self._table.short_url == short_url)
        result = (await self._db_session.execute(q)).scalars().first()
        print(result)
        return result
