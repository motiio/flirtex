from datetime import datetime
from typing import Optional

from pydantic import Field

from src.config.schemas import ORJSONSchema


class UserLoginRequest(ORJSONSchema):
    init_data: str = Field(alias="initData")


class RefreshTokenRequest(ORJSONSchema):
    refresh_token: str


class AccessTokenResponse(ORJSONSchema):
    access_token: str


class RefreshTokenResponse(ORJSONSchema):
    refresh_token: str


class UserLoginResponse(AccessTokenResponse, RefreshTokenResponse):
    ...


class UserSchema(ORJSONSchema):
    tg_id: int = Field(alias="id")
    tg_username: Optional[str] = Field(alias="username")
    tg_first_name: Optional[str] = Field(alias="first_name")
    tg_last_name: Optional[str] = Field(alias="last_name")
    tg_is_premium: Optional[str] = Field(alias="is_premium")
    tg_language_code: Optional[str] = Field(alias="language_code")


class JWTTokenSchema(ORJSONSchema):
    user: int
    expires_at: datetime


class AccessTokenSchema(JWTTokenSchema):
    access_token: str


class RefreshTokenSchema(JWTTokenSchema):
    id: int
    value: str = Field(str, alias="refresh_token")

    class Config:
        orm_mode = True


class UserRead(ORJSONSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.tg_id = None

    id: int
