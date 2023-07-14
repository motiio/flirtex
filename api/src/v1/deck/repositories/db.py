from typing import Type
from uuid import UUID

from sqlalchemy import and_, delete, or_, select

from src.v1.base.repositories.db import BaseReadOnlyRepository, BaseWriteOnlyRepository
from src.v1.deck.models import Like, Match, Skip, Save
from src.v1.deck.schemas import (
    LikeInCreateSchema,
    MatchInCreateSchema,
    SaveInCreateSchema,
    SkipInCreateSchema,
)


class LikeRepository(
    BaseWriteOnlyRepository[
        LikeInCreateSchema,
        None,
        Like,
    ]
):
    @property
    def _table(self) -> Type[Like]:
        return Like

    async def check_like_from_target_profile(
        self, source_profile: UUID, target_profile: UUID
    ):
        q = select(self._table).where(
            self._table.source_profile == target_profile,
            self._table.target_profile == source_profile,
        )
        return (await self._db_session.execute(q)).scalars().first()

    async def delete_mutual_like(self, source_profile: UUID, target_profile: UUID):
        q = delete(self._table).where(
            or_(
                and_(
                    self._table.source_profile == target_profile,
                    self._table.target_profile == source_profile,
                ),
                and_(
                    self._table.source_profile == source_profile,
                    self._table.target_profile == target_profile,
                ),
            )
        )
        return (await self._db_session.execute(q)).scalars().first()


class SkipRepository(
    BaseWriteOnlyRepository[
        SkipInCreateSchema,
        None,
        Skip,
    ]
):
    @property
    def _table(self) -> Type[Skip]:
        return Skip


class SaveRepository(
    BaseWriteOnlyRepository[
        SaveInCreateSchema,
        None,
        Save,
    ]
):
    @property
    def _table(self) -> Type[Skip]:
        return Save


class MatchRepository(
    BaseWriteOnlyRepository[
        MatchInCreateSchema,
        None,
        Match,
    ],
    BaseReadOnlyRepository,
):
    @property
    def _table(self) -> Type[Match]:
        return Match
