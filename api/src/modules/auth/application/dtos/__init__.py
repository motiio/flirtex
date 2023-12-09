__all__ = [
    "TelegramLoginInDTO",
    "TelegramLoginOutDTO",
    "UpdateTokenOutDTO",
    "UpdateTokenInDTO",
]

from auth.application.dtos.telegram_login import (
    TelegramLoginInDTO,
    TelegramLoginOutDTO,
)
from auth.application.dtos.update_token import UpdateTokenInDTO, UpdateTokenOutDTO
