from aiogram.utils.web_app import safe_parse_webapp_init_data
from pydantic import Field, computed_field

from src.config.settings import settings
from src.core.schemas import BaseSchema
from src.modules.auth.domain.exceptions import InvalidInitData


class TelegramLoginRequestSchema(BaseSchema):
    init_data: str = Field(alias="initData")

    @computed_field
    def tg_login_data(self) -> dict:
        try:
            data = safe_parse_webapp_init_data(
                token=settings.BOT_TOKEN,
                init_data=self.init_data,
            )
            if data.get("user", {}).get("is_bot"):
                raise ValueError
        except ValueError:
            raise InvalidInitData from None
        return data
