__all__ = [
    "TelegramLoginInDTO",
    "TelegramLoginOutDTO",
    "UpdateTokenOutDTO",
    "UpdateTokenInDTO",
]

from src.modules.auth.application.dtos.telegram_login import (
    TelegramLoginInDTO,
    TelegramLoginOutDTO,
)
from src.modules.auth.application.dtos.update_token import UpdateTokenInDTO, UpdateTokenOutDTO
