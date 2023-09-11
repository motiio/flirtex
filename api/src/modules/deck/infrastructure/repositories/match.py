from typing import Type

from sqlalchemy import UUID, select

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.deck.application.repositories import IMatchRepository
from src.modules.deck.domain.entities import Match
from src.modules.deck.infrastructure.models import MatchORM


class MatchRepository(
    BaseSqlAlchemyRepository[
        Match,
        MatchORM,
    ],
    IMatchRepository,
):
    @property
    def _table(self) -> Type[MatchORM]:
        return MatchORM

    @property
    def _entity(self) -> Type[Match]:
        return Match

    async def get_skip_by_profiles(
        self, *, target_profile: UUID, source_profile: UUID
    ) -> Match | None:
        q = select(self._table).where(
            self._table.target_profile == target_profile,
            self._table.source_profile == source_profile,
        )
        result = (await self._db_session.execute(q)).scalars().first()
        return result
