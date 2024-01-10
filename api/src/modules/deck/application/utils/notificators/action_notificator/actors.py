import dramatiq

from src.config.settings import settings

from .broker import action_rabbitmq_broker


@dramatiq.actor(broker=action_rabbitmq_broker, queue_name=settings.RABBITMQ_ACTION_NOTIFIER_QUEUE)
def action_notifier(message: str):
    pass
