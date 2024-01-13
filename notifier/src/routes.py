import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError

from src.config.rabbitmq import rabbitmq_connection
from src.modules.auth import check_token_signature

ws_router = APIRouter()

ws_connections: dict[str, WebSocket] = {}


@ws_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    access_token: str,
):
    await websocket.accept()
    try:
        _, data = check_token_signature(token=access_token)
    except JWTError:
        await websocket.close(code=1008, reason="Invalid token")
        return

    user_id_str: str = data.get("sub")
    ws_connections[user_id_str] = websocket
    try:
        if not rabbitmq_connection.queue:
            await websocket.close(code=1011, reason="Source init error")

        async with rabbitmq_connection.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(
                    requeue=True
                ):  # Управление подтверждением вручную
                    kwargs = message.body.decode()

                    # Парсим строку JSON в словарь Python
                    message_dict = json.loads(kwargs)

                    # Извлекаем поле 'message'
                    message_content = message_dict.get("kwargs", {}).get(
                        "message", "{}"
                    )

                    # Парсим строку JSON в словарь Python
                    message = json.loads(message_content)
                    if user_id_str == message.get("recipient"):
                        await ws_connections[user_id_str].send_json(message)
                        await message.ack()

    except WebSocketDisconnect:
        ws_connections.pop(user_id_str, None)  # Безопасное удаление
