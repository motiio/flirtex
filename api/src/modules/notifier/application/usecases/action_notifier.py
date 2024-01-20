from src.core.usecases import IUseCase
from src.modules.notifier.application.domain.entities.de.message import BaseMessage
from src.modules.notifier.application.repositories.redis_notifier import (
    IActionNotificationRepository,
)


class ActionNotifierUsecase(IUseCase):
    def __init__(
        self,
        *,
        notification_repository: IActionNotificationRepository,
    ):
        self._notification_repo: IActionNotificationRepository = notification_repository

    async def execute(self, *, stream_name: str, message: BaseMessage) -> None:
        async with self._notification_repo:
            await self._notification_repo.send_message(stream_name=stream_name, message=message)
