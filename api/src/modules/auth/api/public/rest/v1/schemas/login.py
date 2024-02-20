from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data
from pydantic import Field, computed_field

from src.config.settings import settings
from src.core.schemas import BaseSchema
from src.modules.auth.domain.exceptions import InvalidInitData


class TelegramLoginRequestSchema(BaseSchema):
    init_data: str = Field(alias="initData")

    @computed_field
    @property
    def validated_init_data(self) -> WebAppInitData:
        try:
            data = safe_parse_webapp_init_data(
                token=settings.BOT_TOKEN,
                init_data=self.init_data,
            )
            if not data.user:
                raise ValueError
            elif data.user.is_bot:
                raise ValueError
        except ValueError:
            raise InvalidInitData from None
        return data
