__all__ = [
    # login
    "TelegramLoginInDTO",
    "TelegramLoginOutDTO",
    # update token
    "UpdateTokenOutDTO",
    "UpdateTokenInDTO",
]

from .telegram_login import (
    TelegramLoginInDTO,
    TelegramLoginOutDTO,
)
from .update_token import UpdateTokenInDTO, UpdateTokenOutDTO
