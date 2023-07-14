from typing import Generic, List, Optional, TypeVar, cast, Union
from uuid import UUID, uuid4

from sqlalchemy import delete, inspect, select, update

from src.v1.base.aio import AsyncContextManagerRepository
from src.v1.base.interfaces import IReadOnlyDbRepository, IWriteOnlyDbRepository
from src.v1.base.models import Base
from src.v1.base.schemas import BaseSchema
from src.v1.config.database import DbSession

IN_CREATE_SCHEMA = TypeVar("IN_CREATE_SCHEMA", bound=Union[BaseSchema, None])
IN_UPDATE_SCHEMA = TypeVar("IN_UPDATE_SCHEMA", bound=Union[BaseSchema, None])
TABLE = TypeVar("TABLE", bound=Base)


class BaseReadOnlyRepository(
    AsyncContextManagerRepository,
    IReadOnlyDbRepository,
    Generic[TABLE,],
):
    def __init__(
        self,
        *,
        db_session: DbSession,
    ) -> None:
        self._db_session = db_session

    async def get(self, *, entry_id: UUID) -> Optional[TABLE]:
        entry = await self._db_session.get(entity=self._table, ident=entry_id)
        return entry

    async def fetch(self, *, entry_ids: List[UUID]) -> List[TABLE]:  # type: ignore
        q = select(self._table).where(self._table.id.in_(entry_ids))
        entries = await self._db_session.execute(q)
        return [cast(TABLE, entry) for entry in entries.scalars().all()]

    async def commit(self):
        await self._db_session.commit()

    async def list(self) -> Optional[List[TABLE]]:  # type: ignore
        q = select(self._table)
        entries = await self._db_session.execute(q)
        return [cast(TABLE, entry) for entry in entries.scalars().all()]


class BaseWriteOnlyRepository(
    AsyncContextManagerRepository,
    IWriteOnlyDbRepository,
    Generic[IN_CREATE_SCHEMA, IN_UPDATE_SCHEMA, TABLE],
):
    def __init__(
        self,
        *,
        db_session: DbSession,
    ) -> None:
        self._db_session = db_session

    async def create(self, *, in_schema: IN_CREATE_SCHEMA) -> TABLE:
        inst = inspect(self._table)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]

        entry = self._table(**in_schema.model_dump())
        if "id" in attr_names:
            entry = self._table(id=uuid4(), **in_schema.model_dump())

        self._db_session.add(entry)
        return entry

    async def delete(self, *, entry_id: UUID) -> Optional[TABLE]:
        q = delete(self._table).where(self._table.id == entry_id).returning(self._table)
        entry = (await self._db_session.execute(q)).scalars().first()
        return entry

    async def update(self, *, in_schema: IN_UPDATE_SCHEMA) -> Optional[TABLE]:  # type: ignore
        q = (
            update(self._table)
            .where(self._table.id == in_schema.id)  # type: ignore
            .values(**in_schema.model_dump())
            .returning(self._table)
        )
        entry = (await self._db_session.execute(q)).scalars().first()
        return entry

    async def commit(self):
        await self._db_session.commit()
