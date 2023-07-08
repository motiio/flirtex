from typing import Type
from uuid import UUID
from pydantic_core.core_schema import int_schema

from sqlalchemy import delete, select, update
from sqlalchemy.orm import selectinload
from src.v1.photo.models import Photo

from src.v1.profile.models import Profile
from src.v1.profile.schemas import (
    ProfileInCreateSchema,
    ProfileInUpdateSchema,
)
from src.v1.base.repositories.db import (
    BaseReadOnlyRepository,
    BaseWriteOnlyRepository,
)


class ProfileRepository(
    BaseWriteOnlyRepository[
        ProfileInCreateSchema,
        ProfileInUpdateSchema,
        Profile,
    ],
    BaseReadOnlyRepository[Profile],
):
    @property
    def _table(self) -> Type[Profile]:
        return Profile

    async def get_by_owner(self, *, owner_id: UUID) -> Profile:
        q = (
            select(self._table)
            .where(self._table.owner_id == owner_id)
            .options(selectinload(self._table.interests))
            .options(
                selectinload(
                    self._table.photos.and_(
                        Photo.short_url.isnot(None),
                        Photo.short_url.isnot(None),
                    )
                )
            )
        )
        return (await self._db_session.execute(q)).scalars().first()

    async def delete_by_owner(self, *, owner_id: UUID) -> None:
        q = delete(self._table).where(self._table.owner_id == owner_id)
        await self._db_session.execute(q)

    async def update_by_owner(
        self,
        *,
        in_schema: ProfileInUpdateSchema,
        owner_id: UUID,
    ) -> Profile:
        q = (
            update(self._table)
            .where(self._table.owner_id == owner_id)  # type: ignore
            .options(selectinload(self._table.interests))
            .values(**in_schema.model_dump())
            .returning(self._table)
        )
        entry = (await self._db_session.execute(q)).scalars().first()
        return entry
