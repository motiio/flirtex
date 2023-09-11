from typing import Generic, List
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from src.config.database import DbSession
from src.core.repositories import ISqlAlchemyRepository
from src.core.types import ENTITY, TABLE


class BaseSqlAlchemyRepository(
    ISqlAlchemyRepository,
    Generic[ENTITY, TABLE],
):
    def __init__(self, *, db_session: DbSession) -> None:
        self._db_session = db_session
        self._trans = None

    async def get(self, *, entity_id: UUID) -> ENTITY | None:
        q = select(self._table).where(self._table.id == entity_id)
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
            return self._entity.create(**result.dict())
        return None

    async def fetch(self, *, entities_ids: List[UUID]) -> List[ENTITY]:  # type: ignore
        q = select(self._table).where(self._table.id.in_(entities_ids))
        entries = (await self._db_session.execute(q)).scalars().all()
        return [self._entity.create(**entry.dict()) for entry in entries]

    async def list(self) -> List[ENTITY]:  # type: ignore
        q = select(self._table)
        entities = await self._db_session.execute(q)
        return [
            self._entity.create(**entity.dict()) for entity in entities.scalars().all()
        ]

    async def create(self, *, in_entity: ENTITY) -> ENTITY:
        q = insert(self._table).values(**in_entity.model_dump()).returning(self._table)
        result = (await self._db_session.execute(q)).scalars().one()
        return self._entity.create(**result.dict())

    async def delete(self, *, entity_id: UUID) -> ENTITY:
        q = (
            delete(self._table)
            .where(self._table.id == entity_id)
            .returning(self._table)
        )
        result = (await self._db_session.execute(q)).scalars().one()
        return self._entity.create(**result.dict())

    async def update(self, *, in_entity: ENTITY) -> ENTITY | None:  # type: ignore
        q = (
            update(self._table)
            .where(self._table.id == in_entity.id)  # type: ignore
            .values(**in_entity.model_dump())
            .returning(self._table)
        )
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
            return self._entity.create(**result.dict())
        return None

    async def commit(self):
        await self._db_session.commit()

    async def __aenter__(self):
        if not self._db_session.in_transaction():
            await self._db_session.begin()
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            # TODO добавить логирование
            await self.rollback()
        await self.commit()

    async def rollback(self):
        await self._db_session.rollback()
