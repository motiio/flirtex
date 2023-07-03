from typing import Type
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import selectinload

from src.v1.profile.models import Profile
from src.v1.profile.schemas.profile import ProfileInCreateSchema, ProfileInUpdateSchema
from src.v1.repositories import BaseRepository


class ProfileRepository(
    BaseRepository[
        ProfileInCreateSchema,
        ProfileInUpdateSchema,
        Profile,
    ]
):
    @property
    def _table(self) -> Type[Profile]:
        return Profile

    async def get_by_owner(self, *, owner_id: UUID) -> Profile:
        q = (
            select(self._table)
            .where(self._table.owner_id == owner_id)
            .options(selectinload(self._table.interests))
        )

        return (await self._db_session.execute(q)).scalars().first()

    async def delete_by_owner(self, *, owner_id: UUID) -> None:
        q = delete(self._table).where(self._table.owner_id == owner_id)
        await self._db_session.execute(q)

    async def update_by_owner(self, *, in_schema: ProfileInUpdateSchema, owner_id: UUID) -> Profile:
        q = (
            update(self._table)
            .where(self._table.owner_id == owner_id)  # type: ignore
            .options(selectinload(self._table.interests))
            .values(**in_schema.model_dump())
            .returning(self._table)
        )
        entry = (await self._db_session.execute(q)).scalars().first()
        return entry
