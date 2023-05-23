from datetime import date

from src.config.schemas import ORJSONSchema


class ProfileSchema(ORJSONSchema):
    id: int
    name: str
    birthdate: date
    city: int
    looking_gender: str


class ProfileCreateSchema(ORJSONSchema):
    name: str
    birthdate: date
    city: int
    looking_gender: str


class ProfileReadSchema(ProfileSchema):
    city: str
