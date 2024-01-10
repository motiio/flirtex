from typing import Optional, Type

from sqlalchemy import UUID, and_, case, desc, func, or_, select, text, delete

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.core.types import Pagination
from src.modules.deck.application.repositories import ILikeRepository
from src.modules.deck.domain.entities import Like
from src.modules.deck.infrastructure.models import LikeORM, MatchORM, SkipORM
from src.modules.profile.infrastructure.models import ProfileORM


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

    async def delete_by_target(self, *, source_profile: UUID, target_profile: UUID) -> Like | None:
        q = (
            delete(self._table)
            .where(
                and_(
                    self._table.source_profile == source_profile,
                    self._table.target_profile == target_profile,
                )
            )
            .returning(self._table)
        )
        result = (await self._db_session.execute(q)).scalars().first()
        if result:
         return self._entity.create(**result.dict())
        return None

    async def get_likes_by_profiles(
        self, *, target_profile: UUID, source_profile: UUID
    ) -> tuple[Like | None, Like | None]:
        """
        Запрос находит лайк между 2 профилями и возвращает 2 лайка.
        1 - Лайк, поставленные source_profile или None
        2 - Лайк, поставелнные target_profile или None
        """
        ordering = case({self._table.source_profile == source_profile: 1}, else_=0).label(
            "ordering"
        )

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
        other_like = next((like for like, order in likes_ordering if like != my_like), None)

        return (my_like, other_like)

    async def get_likes_by_target_except_match(
        self,
        *,
        target_profile_id: UUID,
        offset: int = 0,
        limit: int = 30,
        order_by: Optional[str] = None,
    ) -> tuple[list[Like], Pagination]:
        q = (
            select(self._table, ProfileORM)
            .join(ProfileORM, self._table.source_profile == ProfileORM.id)
            .outerjoin(
                MatchORM,
                or_(
                    and_(
                        MatchORM.profile_1 == self._table.source_profile,
                        MatchORM.profile_2 == self._table.target_profile,
                    ),
                    and_(
                        MatchORM.profile_1 == self._table.target_profile,
                        MatchORM.profile_2 == self._table.source_profile,
                    ),
                ),
            )
            .outerjoin(
                SkipORM,
                and_(
                    SkipORM.target_profile == self._table.source_profile,
                    SkipORM.source_profile == self._table.target_profile,
                ),
            )
            .where(
                and_(
                    and_(self._table.target_profile == target_profile_id, MatchORM.id.is_(None)),
                    SkipORM.id.is_(None),
                )
            )
        )
        total_count_query = select(func.count()).select_from(q)  # type: ignore
        total: int = (await self._db_session.execute(total_count_query)).scalar() or 0

        # Добавляем сортировку, если параметр order_by предоставлен
        if order_by is not None:
            if order_by.startswith("-"):  # Проверка на сортировку по убыванию
                q = q.order_by(desc(text(order_by[1:])))  # Отрезаем '-' для desc сортировки
            else:
                q = q.order_by(text(order_by))  # Используем как есть для asc сортировки

        q = q.offset(offset).limit(limit)

        entries = (await self._db_session.execute(q)).scalars().all()
        return [self._entity.create(**entry.dict()) for entry in entries], Pagination(
            total=total, limit=limit, offset=offset
        )
