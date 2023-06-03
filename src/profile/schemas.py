from datetime import date

from pydantic import Field

from src.common.schemas import InterestReadSchema
from src.config.schemas import ORJSONSchema

from .models import GenderEnum


class BaseUserProfileSchema(ORJSONSchema):
    owner: int
    owner: int
    name: str
    birthdate: date
    city: int
    looking_gender: GenderEnum | int
    gender: GenderEnum | int


class UserProfileCreateRequest(ORJSONSchema):
    name: str
    birthdate: date
    # city: int
    looking_gender: GenderEnum | int
    gender: GenderEnum | int
    interests: list[int] = Field(..., min_items=7)


class UserProfileReadSchema(ORJSONSchema):
    id: int
    name: str
    birthdate: date
    looking_gender: GenderEnum | int
    gender: GenderEnum | int

    class Config:
        orm_mode = True


class UserFullProfileReadSchema(UserProfileReadSchema):
    interests: list[InterestReadSchema]

    class Config:
        orm_mode = True
