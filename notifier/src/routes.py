import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError
from src.modules.auth import check_token_signature

from src.config.redis import RedisSession
import redis

ws_router = APIRouter()


async def send_messages_from_redis_stream(
    *, r, stream_name, group_name, consumer_name, websocket, last_id="0"
):
    try:
        await r.xgroup_create(stream_name, group_name, id="0", mkstream=True)
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
                print(message)
                await websocket.send_json(message)
                print(last_id)
                last_id = message_id
                print(last_id)


async def delete_message_id_from_stream(
    websocket: WebSocket, stream_name, r, group_name
):
    while True:
        try:
            # Receive message ID from client
            response = await websocket.receive_json()
            # Delete the message ID from the stream
            print(response)
            if (message_id := response.get("message_id")) is None:
                continue
            print(message_id)
            action=response.get("action", 'ack')
            print(action)
            await r.xack(stream_name, group_name, message_id)
            if action == 'del':
                await r.xdel(stream_name, message_id)

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

    stream_name: str = data.get("sub")
    group_name: str = "notifier_service_group"
    consumer_name: str = "notifier_service"

    try:
        print(0)
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
        print(1)
        await asyncio.gather(del_mesagges_task, send_message_task)
        print(2)
    finally:
        await websocket.close()
