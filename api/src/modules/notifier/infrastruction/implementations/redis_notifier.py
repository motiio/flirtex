
from src.config.settings import settings
from src.core.repositories.implementations.redis import BaseRedisRepository
from src.modules.notifier.application.domain.entities import BaseMessage
from src.modules.notifier.application.repositories import IActionNotificationRepository


class ActionNotificationRepository(BaseRedisRepository, IActionNotificationRepository):
    async def send_message(
        self,
        *,
        stream_name: str,
        message: BaseMessage,
        ttl: int = settings.REDIS_STREAM_TTL_S,
    ):
        await self._session.xadd(name=stream_name, fields={"message": message.model_dump_json()})
