from typing import Type
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.v1.repositories import BaseRepository
from src.v1.profile.models import Interest, Profile
from src.v1.profile.schemas.profile import ProfileInCreateSchema, ProfileInUpdateSchema


class ProfileRepository(
    BaseRepository[ProfileInCreateSchema, ProfileInUpdateSchema, Profile]
):
    @property
    def _table(self) -> Type[Profile]:
        return Profile

    async def create(
        self, *, in_schema: ProfileInCreateSchema, interests: list[Interest]
    ) -> Profile:
        profile = Profile(**in_schema.model_dump(exclude={"interests"}))
        profile.interests = interests
        self._db_session.add(profile)
        return profile

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

    async def update(
        self,
        *,
        in_schema: ProfileInUpdateSchema,
        interests: list[Interest],
    ) -> Profile:
        profile = await self.get_by_owner(owner_id=in_schema.owner_id)

        profile.bio = in_schema.bio
        if interests is not None:
            profile.interests = interests

        return profile
