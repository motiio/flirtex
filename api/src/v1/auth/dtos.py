from uuid import UUID

import orjson
from aiogram.utils.web_app import safe_parse_webapp_init_data
from pydantic import Field, computed_field

from src.v1.auth.exceptions import InvalidInitData
from src.v1.auth.utils import jwt
from src.v1.config.schemas import BaseSchema
from src.v1.config.settings import settings

###############################################################
#                Request data transfer objects                #
###############################################################


class InitDataRequestLogin(BaseSchema):
    init_data: str = Field(alias="initData")

    @computed_field
    @property
    def valid_init_data(self) -> dict:
        try:
            data = safe_parse_webapp_init_data(
                token=settings.BOT_TOKEN,
                init_data=self.init_data,
                _loads=orjson.loads,
            )
            if data.get("user", {}).get("is_bot"):
                raise ValueError
        except ValueError:
            raise InvalidInitData from None
        return data


class RefreshTokenRequestUpdateTokenPair(BaseSchema):
    value: str = Field(alias="refresh_token")

    @computed_field
    @property
    def valid_token_data(
        self,
    ) -> dict:
        valid_token, data = jwt.check_token_signature(token=self.value)
        return {"value": str(valid_token), "user": UUID(data["sub"])}


################################################################
#                Response data transfer objects                #
################################################################


class TokenPairResponse(BaseSchema):
    access_token: str
    refresh_token: str
