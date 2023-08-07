from abc import ABC, abstractmethod

from src.core.aio import IAsyncContextManagerRepository
from src.modules.auth.domain.entities.de.user import User


class IUserRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def get(self, *, entity_id) -> User:
        ...

    @abstractmethod
    async def get_by_tg_id(self, *, tg_id: int) -> User | None:
        ...
