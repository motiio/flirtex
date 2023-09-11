from typing import Type

from sqlalchemy import UUID, select

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.deck.application.repositories import ISkipRepository
from src.modules.deck.domain.entities import Skip
from src.modules.deck.infrastructure.models import SkipORM


class SkipRepository(
    BaseSqlAlchemyRepository[
        Skip,
        SkipORM,
    ],
    ISkipRepository,
):
    @property
    def _table(self) -> Type[SkipORM]:
        return SkipORM

    @property
    def _entity(self) -> Type[Skip]:
        return Skip

    async def get_skip_by_profiles(
        self, *, target_profile: UUID, source_profile: UUID
    ) -> Skip | None:
        q = select(self._table).where(
            self._table.target_profile == target_profile,
            self._table.source_profile == source_profile,
        )
        result = (await self._db_session.execute(q)).scalars().first()
        return result
