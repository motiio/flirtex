from uuid import UUID

from sqlalchemy import column, func, select

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.deck.application.repositories.deck import IDeckRepository


class DeckRepository(
    BaseSqlAlchemyRepository[
        None,  # type: ignore
        None,
    ],
    IDeckRepository,
):
    @property
    def _table(self) -> None:
        return None

    def _entity(self) -> None:
        return None

    async def generate(self, *, profile_id: UUID) -> list[UUID]:
        q = select(column("profile_id")).select_from(func.core.deck(profile_id))
        deck = await self._db_session.execute(q)

        return list(deck.scalars().all())
