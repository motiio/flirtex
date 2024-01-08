from typing import Type

from sqlalchemy import UUID, and_, desc, func, or_, select, text

from src.core.orm import DictBundle
from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.core.types import Pagination
from src.modules.deck.application.repositories import IMatchRepository
from src.modules.deck.domain.entities import Match, MatchProfileDAE
from src.modules.deck.infrastructure.models import MatchORM
from src.modules.profile.infrastructure.models import PhotoORM, ProfileORM
from src.modules.profile.application.dependencies import AuthAPI


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

    @property
    def _match_profile_dae(self) -> Type[MatchProfileDAE]:
        return MatchProfileDAE

    async def get_match_profiles(
        self,
        *,
        profile_id: UUID,
        limit: int = 30,
        offset: int = 0,
        order_by: str | None = None,
    ) -> tuple[list[MatchProfileDAE], Pagination]:
        q = (
            select(
                DictBundle(
                    "match_profile_dae",
                    self._table.id.label("match_id"),
                    ProfileORM.id.label("profile_id"),
                    ProfileORM.name.label("profile_name"),
                    ProfileORM.bio.label("profile_bio"),
                    PhotoORM.url.label("profile_main_photo_url"),
                    AuthAPI.table.tg_username.label("user_tg_username"), # type: ignore
                ),
            )
            .join(
                ProfileORM,
                or_(ProfileORM.id == self._table.profile_1, ProfileORM.id == self._table.profile_2),
            )
            .join(AuthAPI.table, ProfileORM.owner_id == AuthAPI.table.id) # type: ignore
            .outerjoin(
                PhotoORM, and_(ProfileORM.id == PhotoORM.profile_id, PhotoORM.displaying_order == 1)
            )
            .where(ProfileORM.id != profile_id)
        )
        print(q)

        total_count_query = select(func.count()).select_from(q)  # type: ignore
        total: int = (await self._db_session.execute(total_count_query)).scalar() or 0

        # Добавляем сортировку, если параметр order_by предоставлен
        if order_by is not None:
            if order_by.startswith("-"):  # Проверка на сортировку по убыванию
                q = q.order_by(desc(text(order_by[1:])))  # Отрезаем '-' для desc сортировки
            else:
                q = q.order_by(text(order_by))  # Используем как есть для asc сортировки

        entries = await self._db_session.execute(q)
        return [
            self._match_profile_dae.create(**entry.match_profile_dae) for entry in entries
        ], Pagination(total=total, offset=offset, limit=limit)
