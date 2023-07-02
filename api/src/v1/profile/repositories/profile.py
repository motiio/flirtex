from typing import Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.v1.config.repositories import BaseRepository
from src.v1.profile.models import Interest, Profile
from src.v1.profile.schemas.profile import ProfileInCreateSchema


class ProfileRepository(BaseRepository[ProfileInCreateSchema, Profile]):
    @property
    def _table(self) -> Type[Profile]:
        return Profile

    async def create(
        self, *, in_schema: ProfileInCreateSchema, interests: Interest
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
