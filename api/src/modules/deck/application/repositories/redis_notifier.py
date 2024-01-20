from abc import ABC, abstractmethod

from src.config.settings import settings
from src.core.aio import IAsyncContextManagerRepository
from src.modules.notifier.application.domain.entities.de.message import BaseMessage


class IActionNotificationRepository(IAsyncContextManagerRepository, ABC):
    @abstractmethod
    async def send_message(
        self, *, stream_name: str, message: BaseMessage, ttl: int = settings.REDIS_STREAM_TTL_S
    ) -> None:
        ...
