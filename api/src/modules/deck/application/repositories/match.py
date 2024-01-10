from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.core.types import Pagination
from src.modules.deck.domain.entities import Match, MatchProfileDAE


class IMatchRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Match) -> Match:
        ...

    @abstractmethod
    async def get_match_profiles(
        self,
        *,
        profile_id: UUID,
        limit: int = 30,
        offset: int = 0,
        order_by: str | None = None,
    ) -> tuple[list[MatchProfileDAE], Pagination]:
        ...
