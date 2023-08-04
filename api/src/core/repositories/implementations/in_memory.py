from typing import Generic, List, Type
from uuid import UUID

from src.core.repositories import ISqlAlchemyRepository
from src.core.types import ENTITY, TABLE


class BaseInMemorySqlAlchemnyRepository(
    ISqlAlchemyRepository,
    Generic[ENTITY, TABLE],
):
    def __init__(self, *, db_session: dict) -> None:
        self._db_session: dict[UUID, Type[TABLE]] = db_session

    async def get(self, *, entity_id: UUID) -> ENTITY | None:
        result = self._db_session.get(entity_id)
        if result:
            return self._entity.create(**result.dict())
        return None

    async def fetch(self, *, entities_ids: List[UUID]) -> List[ENTITY] | None:  # type: ignore
        entries = [value for key, value in self._db_session.items() if key in entities_ids]
        return [self._entity.create(**entry.dict()) for entry in entries]

    async def list(self) -> List[ENTITY] | None:  # type: ignore
        entities = self._db_session.values()
        return [self._entity.create(**entity.dict()) for entity in entities]

    async def create(self, *, in_entity: ENTITY) -> ENTITY:
        inserted_obj = self._table(**in_entity.model_dump())
        self._db_session[in_entity.id] = inserted_obj
        result = self._db_session[in_entity.id]
        return self._entity.create(**result.dict())

    async def delete(self, *, entity_id: UUID) -> ENTITY | None:
        result = self._db_session.get(entity_id)

        if result:
            del self._db_session[entity_id]
            return self._entity.create(**result.dict())

        return None

    async def update(self, *, in_entity: ENTITY) -> ENTITY | None:  # type: ignore
        if self._db_session.get(in_entity.id):
            result = self._db_session[in_entity.id] = self._table(**in_entity.model_dump())

            if result:
                return self._entity.create(**result.model_dump())

    async def commit(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            # TODO добавить логирование
            await self.rollback()
        await self.commit()

    async def rollback(self):
        pass
