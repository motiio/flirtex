from aiogram.utils.web_app import WebAppInitData

from src.core.dtos import BaseDTO


class TelegramLoginInDTO(BaseDTO):
    web_app_init_data: WebAppInitData
    user_agent: str


class TelegramLoginOutDTO(BaseDTO):
    refresh_token: str
    access_token: str
