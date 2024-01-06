from abc import ABC, abstractmethod
from uuid import UUID

from src.core.aio import IAsyncContextManagerRepository
from src.core.types import Pagination
from src.modules.deck.domain.entities import Match


class IMatchRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Match) -> Match:
        ...

    @abstractmethod
    async def get_match_profiles(
        self,
        *,
        profile_id: UUID,
        order_by: str | None = None,
    ) -> tuple[list[Match], Pagination]:
        ...
