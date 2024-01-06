from src.core.dtos import BaseDTO


class TelegramLoginInDTO(BaseDTO):
    tg_login_data: dict
    user_agent: str


class TelegramLoginOutDTO(BaseDTO):
    refresh_token: str
    access_token: str
