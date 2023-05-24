from datetime import date

from src.config.schemas import ORJSONSchema

from .models import GenderEnum


class BaseProfileSchema(ORJSONSchema):
    owner: int
    name: str
    birthdate: date
    city: int
    looking_gender: GenderEnum | int
    gender: GenderEnum | int


class ProfileCreateRequest(ORJSONSchema):
    name: str
    birthdate: date
    city: int
    looking_gender: GenderEnum | int
    gender: GenderEnum | int


class ProfileReadSchema(ORJSONSchema):
    name: str
    birthdate: date
    city: int
    looking_gender: GenderEnum | int
    gender: GenderEnum | int

    class Config:
        orm_mode = True
