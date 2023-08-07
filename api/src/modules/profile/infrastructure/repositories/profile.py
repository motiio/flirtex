from typing import Type
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.profile.application.repositories import IProfileRepository
from src.modules.profile.domain.entities import Interest, Profile
from src.modules.profile.domain.entities.dae.profile_photo import PhotoDAE
from src.modules.profile.infrastructure.models import InterestORM, ProfileORM


class ProfileRepository(
    BaseSqlAlchemyRepository[
        Profile,
        ProfileORM,
    ],
    IProfileRepository,
):
    @property
    def _table(self) -> Type[ProfileORM]:
        return ProfileORM

    @property
    def _entity(self) -> Type[Profile]:
        return Profile

    async def create(
        self, *, in_entity: Profile, interests_ids: list[UUID] | None
    ) -> Profile:
        q = (
            insert(self._table)
            .values(**in_entity.model_dump(exclude={"interests"}))
            .returning(self._table)
            .options(selectinload(self._table.interests))
            .options(selectinload(self._table.photos))
        )

        result = (await self._db_session.execute(q)).scalars().one()

        interests = []
        if interests_ids:
            q = select(InterestORM).where(InterestORM.id.in_(interests_ids))
            interests = (await self._db_session.execute(q)).scalars().all()
        result.interests = interests  # type: ignore

        entity = self._entity.create(**result.dict())
        entity.put_interests(
            [Interest.create(**interest.dict()) for interest in interests]
        )
        return entity

    async def get_by_owner(self, *, owner_id) -> Profile | None:  # type: ignore
        q = (
            select(self._table)
            .where(self._table.owner_id == owner_id)
            .options(selectinload(self._table.interests))
        )
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
            entity: Profile = self._entity.create(**result.dict())
            entity.put_interests(
                [Interest.create(**interest.dict()) for interest in result.interests]
            )
            entity.add_photos(
                [PhotoDAE.create(**photo.dict()) for photo in result.photos]
            )
            return entity

        return None

    async def update(
        self, *, in_entity: Profile, interests_ids: list[UUID] | None
    ) -> Profile:
        q = (
            update(self._table)
            .where(self._table.id == in_entity.id)  # type: ignore
            .values(**in_entity.model_dump(exclude={"interests"}))
            .returning(self._table)
            .options(selectinload(self._table.interests))
        )
        result = (await self._db_session.execute(q)).scalars().one()

        interests = []
        if interests_ids:
            q = select(InterestORM).where(InterestORM.id.in_(interests_ids))
            interests = (await self._db_session.execute(q)).scalars().all()

        result.interests = interests  # type: ignore

        entity = self._entity.create(**result.dict())
        entity.put_interests(
            [Interest.create(**interest.dict()) for interest in result.interests]
        )
        return entity
