from typing import Type

from sqlalchemy import UUID, and_, case, or_, select

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.deck.application.repositories import ILikeRepository
from src.modules.deck.domain.entities import Like
from src.modules.deck.infrastructure.models import LikeORM


class LikeRepository(
    BaseSqlAlchemyRepository[
        Like,
        LikeORM,
    ],
    ILikeRepository,
):
    @property
    def _table(self) -> Type[LikeORM]:
        return LikeORM

    @property
    def _entity(self) -> Type[Like]:
        return Like

    async def get_likes_by_profiles(
        self, *, target_profile: UUID, source_profile: UUID
    ) -> tuple[Like | None, Like | None]:
        ordering = case(
            {self._table.source_profile == source_profile: 1}, else_=0
        ).label("ordering")

        q = select(self._table, ordering).where(
            or_(
                and_(
                    self._table.target_profile == target_profile,
                    self._table.source_profile == source_profile,
                ),
                and_(
                    self._table.source_profile == target_profile,
                    self._table.target_profile == source_profile,
                ),
            )
        )
        result = await self._db_session.execute(q)
        records = result.all()
        likes_ordering = [(record[0], record[1]) for record in records]

        my_like = next((like for like, order in likes_ordering if order == 1), None)
        other_like = next(
            (like for like, order in likes_ordering if like != my_like), None
        )

        return (my_like, other_like)
