from src.core.schemas import BaseSchema


class TelegramLoginOutSchema(BaseSchema):
    refresh_token: str
    access_token: str


