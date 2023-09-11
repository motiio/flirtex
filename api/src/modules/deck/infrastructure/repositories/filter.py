from typing import Type

from sqlalchemy import UUID, select

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.deck.application.repositories.filter import IFilterRepository
from src.modules.deck.domain.entities import Filter
from src.modules.deck.infrastructure.models import FilterORM


class FilterRepository(
    BaseSqlAlchemyRepository[
        Filter,
        FilterORM,
    ],
    IFilterRepository,
):
    @property
    def _table(self) -> Type[FilterORM]:
        return FilterORM

    @property
    def _entity(self) -> Type[Filter]:
        return Filter

    async def get_by_profile(self, *, profile_id: UUID) -> Filter | None:
        q = select(self._table).where(self._table.profile_id == profile_id)
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
            return self._entity.create(**result.dict())
        return None
