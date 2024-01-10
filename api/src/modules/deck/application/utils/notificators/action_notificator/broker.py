from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware.asyncio import AsyncIO

from src.config.settings import settings

action_rabbitmq_broker = RabbitmqBroker(
    url=settings.RABBITMQ_ACTION_NOTIFIER_URL,
    middleware=[AsyncIO()]
)
