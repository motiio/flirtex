from src.config.redis import RedisNotifierSession
from src.modules.notifier.application.usecases.action_notifier import ActionNotifierUsecase
from src.modules.notifier.infrastruction.implementations.redis_notifier import (
    ActionNotificationRepository,
)


def action_notification_service_factory(redis_session: RedisNotifierSession):
    notification_repository = ActionNotificationRepository(session=redis_session)

    return ActionNotifierUsecase(notification_repository=notification_repository)
