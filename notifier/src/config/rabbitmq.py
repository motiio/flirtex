import asyncio
from dataclasses import dataclass

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractRobustConnection
from fastapi import Request

from .settings import settings


@dataclass
class RabbitMQConnection:
    host_url: str
    queue_name: str
    connection: AbstractRobustConnection | None = None
    channel: AbstractChannel | None = None
    queue: AbstractQueue | None = None
    is_durable: bool = True
    dead_letter_routing_key: str = "XQ"

    async def disconnect(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(
        self,
        *,
        connection: AbstractRobustConnection | None = None,
        max_retries=5,
        delay=10,
    ):
        for attempt in range(max_retries):
            try:
                self.connection = connection or (
                    await aio_pika.connect_robust(self.host_url)
                )
                self.channel = await self.connection.channel()
                self.queue = await self.channel.declare_queue(
                    self.queue_name,
                    durable=self.is_durable,
                    arguments={
                        "x-dead-letter-routing-key": self.dead_letter_routing_key,
                        "x-dead-letter-exchange": "",
                    },
                )
                return self
            except (OSError, ConnectionRefusedError) as e:
                print(
                    f"Не удалось подключиться к RabbitMQ (попытка {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay)
        raise RuntimeError("Error trying to connect to RabbitMQ")


def get_rabbitmq_connection(request: Request):
    return request.state.match_notifier_connection


rabbitmq_connection = RabbitMQConnection(
    host_url=settings.RABBITMQ_URL,
    queue_name=settings.RABBITMQ_QUEUE,
    is_durable=settings.IS_DURABLE,
    dead_letter_routing_key=settings.X_DEAD_LETTER_ROUTING_KEY,
)
