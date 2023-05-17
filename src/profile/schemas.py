from datetime import date
from typing import Optional

from pydantic import Field

from src.config.schemas import ORJSONSchema


class UserLogin(ORJSONSchema):
    init_data: str = Field(alias="initData")


class UserLoginResponse(ORJSONSchema):
    token: Optional[str] = Field(None, nullable=True)


class ProfileRead(ORJSONSchema):
    id: int
    name: str
    birthdate: date
    city: str
    looking_gender: str
