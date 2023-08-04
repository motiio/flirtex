from abc import ABCMeta, abstractmethod
from typing import Generic, Type, List, TypeVar
from src.core.types import ENTITY, TABLE
from uuid import UUID
from src.core.aio import IAsyncContextManagerRepository


class IRepository(
    Generic[ENTITY, TABLE],
    metaclass=ABCMeta,
):
    @abstractmethod
    async def get(self, *, entity_id: UUID) -> ENTITY | None:
        ...

    @abstractmethod
    async def list(self) -> List[ENTITY] | None:
        ...

    @abstractmethod
    async def fetch(self, *, entity_ids: List[UUID]) -> List[ENTITY] | None:
        ...

    @abstractmethod
    async def create(self, *, in_entity: ENTITY) -> ENTITY:
        ...

    @abstractmethod
    async def update(self, *, in_entity: ENTITY) -> List[ENTITY]:
        ...

    @abstractmethod
    async def delete(self, *, entity_id: UUID) -> ENTITY:
        ...


REPOSITORY = TypeVar("REPOSITORY", bound=IRepository)


class ISqlAlchemyRepository(
    IRepository,
    IAsyncContextManagerRepository,
    Generic[ENTITY, TABLE],
    metaclass=ABCMeta,
):
    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        raise NotImplemented

    @property
    @abstractmethod
    def _entity(self) -> Type[ENTITY]:
        raise NotImplemented

        # class IS3Repository(
        #     IRepository,
        #     Generic[
        #         IN_DTO,
        #         OUT_DTO,
        #     ],
        #     metaclass=ABCMeta,
        # ):
        #     @property
        #     @abstractmethod
        #     async def _bucket(self):
        ...
