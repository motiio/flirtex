from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Generic, Type, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import delete, select

from src.database.core import DbSession
from src.v1.config.exceptions import DoesNotExists
from src.v1.config.models import Base
from src.v1.config.schemas import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=Base)


class AsyncContextManagerRepository(metaclass=ABCMeta):
    @abstractmethod
    async def commit(self):
        ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.commit()


class BaseRepository(
    AsyncContextManagerRepository,
    Generic[IN_SCHEMA, TABLE],
    metaclass=ABCMeta,
):
    db_session: DbSession

    def __init__(
        self,
        *,
        db_session: DbSession,
    ) -> None:
        self._db_session = db_session

    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    async def create(self, *, in_schema: IN_SCHEMA) -> TABLE:
        entry = self._table(id=uuid4(), **in_schema.model_dump())
        self._db_session.add(entry)
        return entry

    async def get(self, *, entry_id: UUID) -> TABLE | None:
        entry = await self._db_session.get(entity=self._table, ident=entry_id)
        if not entry:
            raise DoesNotExists(f"{self._table}[id={entry_id}]")

        return entry

    async def list(self, *, entry_ids: list[UUID]) -> list[TABLE]:
        q = select(self._table).where(self._table.id.in_(entry_ids))
        entrys = (await self._db_session.execute(q)).all()
        return [entry[0] for entry in entrys]

    async def delete(self, *, entry_id: UUID) -> TABLE | None:
        q = delete(self._table).where(self._table.id == entry_id).returning(self._table)
        entry = (await self._db_session.execute(q)).scalars().first()
        return entry

    async def commit(self):
        await self._db_session.commit()
