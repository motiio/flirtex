from datetime import date

from pydantic import Field

from src.common.schemas import InterestOutResponse
from src.config.schemas import ORJSONSchema

from .models import GenderEnum


class ProfileInRegistration(ORJSONSchema):
    name: str
    birthdate: date
    looking_gender: GenderEnum
    gender: GenderEnum
    interests: list[int] = Field(..., max_items=7)


class ProfileOutResponse(ORJSONSchema):
    id: int
    name: str
    birthdate: date
    looking_gender: GenderEnum
    gender: GenderEnum
    interests: list[InterestOutResponse] | None = None
    photos_url: list[str] | None = None

    class Config:
        orm_mode = True
