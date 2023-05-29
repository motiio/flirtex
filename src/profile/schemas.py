from datetime import date

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
    city: int
    looking_gender: GenderEnum | int
    gender: GenderEnum | int


class UserProfileReadSchema(ORJSONSchema):
    id: int
    name: str
    birthdate: date
    city: int
    looking_gender: GenderEnum | int
    gender: GenderEnum | int

    class Config:
        orm_mode = True
