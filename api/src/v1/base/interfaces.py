from abc import ABCMeta, abstractmethod
from os import walk
from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID
from src.v1.base.schemas import BaseSchema
from src.v1.base.models import Base

IN_CREATE_SCHEMA = TypeVar("IN_CREATE_SCHEMA", bound=BaseSchema)
IN_UPDATE_SCHEMA = TypeVar("IN_UPDATE_SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=Base)


class IReadOnlyRepository(
    Generic[TABLE,],
    metaclass=ABCMeta,
):
    @abstractmethod
    def get(self, *, entry_id: UUID) -> TABLE | None:
        ...

    @abstractmethod
    def list(self) -> List[TABLE]:
        ...

    @abstractmethod
    def fetch(self, *, entry_ids: List[UUID]) -> List[TABLE]:
        ...


class IReadOnlyDbRepository(
    IReadOnlyRepository,
    Generic[TABLE,],
):
    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        ...


class IWriteOnlyRepository(
    Generic[
        IN_CREATE_SCHEMA,
        IN_UPDATE_SCHEMA,
        TABLE,
    ],
    metaclass=ABCMeta,
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


class IWriteOnlyDbRepository(
    IWriteOnlyRepository,
    Generic[
        IN_CREATE_SCHEMA,
        IN_UPDATE_SCHEMA,
        TABLE,
    ],
    metaclass=ABCMeta,
):
    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        ...
