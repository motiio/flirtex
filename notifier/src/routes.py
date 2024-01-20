import asyncio

import redis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError

from src.config.redis import RedisSession
from src.modules.auth import check_token_signature

ws_router = APIRouter()


async def send_messages_from_redis_stream(
    *, r, stream_name, group_name, consumer_name, websocket, last_id="0"
):
    try:
        await r.xgroup_create(stream_name, group_name, id=last_id, mkstream=True)
    except redis.ResponseError as e:
        if not str(e).startswith("BUSYGROUP Consumer Group name already exists"):
            raise
    # Первоначальная загрузка всех непрочитанных сообщений
    while True:
        streams = await r.xreadgroup(
            group_name, consumer_name, {stream_name: last_id}, count=10, block=1000
        )
        if not streams:
            break  # Если нет непрочитанных сообщений, выходим из цикла
        for _, messages in streams:
            for message_id, message in messages:
                await websocket.send_json(message)
                last_id = message_id

    # Переход к чтению новых сообщений
    last_id = ">"
    while True:
        streams = await r.xreadgroup(
            group_name, consumer_name, {stream_name: last_id}, count=1, block=1000
        )
        for _, messages in streams:
            for message_id, message in messages:
                await websocket.send_json(message)
                last_id = message_id


async def delete_message_id_from_stream(
    websocket: WebSocket, stream_name, r, group_name
):
    while True:
        try:
            # Receive message ID from client
            message_id_to_delete = await websocket.receive_text()
            # Delete the message ID from the stream
            await r.xack(stream_name, group_name, message_id_to_delete)
            await r.xdel(stream_name, message_id_to_delete)
        except WebSocketDisconnect:
            break


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, access_token: str, r: RedisSession):
    await websocket.accept()
    try:
        _, data = check_token_signature(token=access_token)
    except JWTError:
        await websocket.close(code=1008, reason="Invalid token")
        return

    stream_name: str = data.get("sub") #type: ignore
    group_name: str = "notifier_service_group"
    consumer_name: str = "notifier_service"

    try:
        del_mesagges_task = asyncio.create_task(
            delete_message_id_from_stream(
                websocket=websocket, r=r, stream_name=stream_name, group_name=group_name
            )
        )
        send_message_task = asyncio.create_task(
            send_messages_from_redis_stream(
                websocket=websocket,
                r=r,
                stream_name=stream_name,
                group_name=group_name,
                consumer_name=consumer_name,
            )
        )
        await asyncio.gather(del_mesagges_task, send_message_task)
    finally:
        await websocket.close()
