from typing import Optional, Type
from uuid import UUID

from geoalchemy2.elements import WKTElement
from sqlalchemy import func, insert, select, update
from sqlalchemy.orm import selectinload

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.profile.application.repositories import IProfileRepository
from src.modules.profile.domain.entities import Interest, Profile, ProfilePhoto
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

    async def get(self, *, entity_id: UUID) -> Profile | None:
        q = (
            select(self._table)
            .where(self._table.id == entity_id)
            .options(selectinload(self._table.interests))
        )
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
            entity: Profile = self._entity.create(**result.dict())
            entity.put_interests(
                [Interest.create(**interest.dict()) for interest in result.interests]
            )
            entity.add_photos(
                [ProfilePhoto.create(**photo.dict()) for photo in result.photos]
            )

            entity.put_location(location=result.dict_location)
            return entity

        return None

    async def create(self, *, in_entity: Profile) -> Profile:
        q = (
            insert(self._table)
            .values(
                **in_entity.model_dump(
                    exclude={
                        "interests",
                        "photos",
                        "age",
                        "location",
                        "wkt_point",
                        "distance",
                    }
                ),
            )
            .returning(
                self._table,
            )
            .options(selectinload(self._table.interests))
            .options(selectinload(self._table.photos))
        )

        result = (await self._db_session.execute(q)).scalars().one()
        entity = self._entity.create(**result.dict())
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
                [ProfilePhoto.create(**photo.dict()) for photo in result.photos]
            )

            entity.put_location(location=result.dict_location)
            return entity

        return None

    async def update(
        self, *, in_entity: Profile, interests_ids: list[UUID] | None
    ) -> Profile:
        geo_point = (
            WKTElement(in_entity.wkt_point, srid=4326) if in_entity.wkt_point else None
        )

        q = (
            update(self._table)
            .where(self._table.id == in_entity.id)  # type: ignore
            .values(
                **in_entity.model_dump(
                    exclude={"interests", "photos", "age", "location", "wkt_point"}
                ),
                location=geo_point,
            )
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
        entity.put_location(location=result.dict_location)
        return entity

    async def fetch(
        self,
        *,
        entities_ids: list[UUID],
        ordering: Optional[bool] = False,
    ) -> list[Profile]:
        q = (
            select(self._table)
            .where(self._table.id.in_(entities_ids))
            .options(selectinload(self._table.interests))
        )
        if ordering:
            q = q.order_by(func.array_position(entities_ids, self._table.id))

        entries = (await self._db_session.execute(q)).scalars().all()
        result: list[Profile] = []
        for entity in entries:
            profile: Profile = self._entity.create(**entity.dict())
            profile.put_interests(
                [Interest.create(**interest.dict()) for interest in entity.interests]
            )
            profile.add_photos(
                [ProfilePhoto.create(**photo.dict()) for photo in entity.photos]
            )

            profile.put_location(location=entity.dict_location)
            result.append(profile)

        return result
