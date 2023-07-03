from abc import ABCMeta, abstractmethod
from typing import Generic, Type, TypeVar, cast, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update

from src.database.core import DbSession
from src.v1.models import Base
from src.v1.schemas import BaseSchema

IN_CREATE_SCHEMA = TypeVar("IN_CREATE_SCHEMA", bound=BaseSchema)
IN_READ_SCHEMA = TypeVar("IN_READ_SCHEMA", bound=BaseSchema)
IN_UPDATE_SCHEMA = TypeVar("IN_UPDATE_SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=Base)


class IReadOnlyRepository(Generic[IN_READ_SCHEMA, TABLE], metaclass=ABCMeta):
    @abstractmethod
    def get(self, *, entry_id: UUID) -> TABLE | None:
        ...

    @abstractmethod
    def list(self, *, entry_ids: List[UUID]) -> List[TABLE]:
        ...

    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        ...


class IWriteOnlyRepository(
    Generic[IN_CREATE_SCHEMA, IN_UPDATE_SCHEMA, TABLE], metaclass=ABCMeta
):
    @abstractmethod
    def create(self, *, in_schema: IN_CREATE_SCHEMA) -> Optional[TABLE]:
        ...

    @abstractmethod
    def update(self, *, in_schema: IN_UPDATE_SCHEMA) -> List[TABLE]:
        ...

    @abstractmethod
    def delete(self, *, entry_id: UUID) -> Optional[TABLE]:
        ...

    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        ...


class AsyncContextManagerRepository(metaclass=ABCMeta):
    @abstractmethod
    async def commit(self):
        ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.commit()


class BaseReadOnlyRepository(
    AsyncContextManagerRepository,
    IReadOnlyRepository,
    Generic[IN_READ_SCHEMA, TABLE],
    metaclass=ABCMeta,
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

    async def list(self, *, entry_ids: Optional[List[UUID]]) -> Optional[List[TABLE]]:  # type: ignore
        if entry_ids is None:
            return None
        q = select(self._table).where(self._table.id.in_(entry_ids))
        entries = await self._db_session.execute(q)
        return [cast(TABLE, entry) for entry in entries.scalars().all()]

    async def commit(self):
        await self._db_session.commit()


class BaseWriteOnlyRepository(
    AsyncContextManagerRepository,
    IWriteOnlyRepository,
    Generic[IN_CREATE_SCHEMA, IN_UPDATE_SCHEMA, TABLE],
    metaclass=ABCMeta,
):
    def __init__(
        self,
        *,
        db_session: DbSession,
    ) -> None:
        self._db_session = db_session

    async def create(self, *, in_schema: IN_CREATE_SCHEMA) -> TABLE:
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


class BaseRepository(
    BaseReadOnlyRepository,
    BaseWriteOnlyRepository,
    Generic[IN_CREATE_SCHEMA, IN_UPDATE_SCHEMA, TABLE],
    metaclass=ABCMeta,
):
    db_session: DbSession

    def __init__(self, *, db_session: DbSession) -> None:
        super().__init__(db_session=db_session)

    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    async def commit(self):
        await self._db_session.commit()
