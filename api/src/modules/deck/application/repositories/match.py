from abc import ABC, abstractmethod

from src.core.aio import IAsyncContextManagerRepository
from src.modules.deck.domain.entities import Match


class IMatchRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def create(self, *, in_entity: Match) -> Match:
        ...
