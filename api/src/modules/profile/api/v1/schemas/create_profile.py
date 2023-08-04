from datetime import date, datetime
from uuid import UUID

from dateutil.relativedelta import relativedelta
from pydantic import Field, field_validator

from src.core.schemas import BaseSchema
from src.modules.profile.application.utils.enums import GenderEnum, LookingGenderEnum


class CreateProfileRequestSchema(BaseSchema):
    name: str = Field(max_length=32)
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    bio: str | None = Field("", max_length=600)
    interests: list[UUID] | None = None

    @field_validator("birthdate")
    def check_legal_age(cls, v):
        years_from_born = relativedelta(datetime.now(), v).years
        if years_from_born < 18:
            raise ValueError("Your age must be 18+")
        elif years_from_born > 100:
            raise ValueError("You're too old, sorry")
        return v

    @field_validator("interests")
    def check_interests_len(cls, v):
        if v is None:
            return v

        if 0 < len(v) < 8:
            return v

        raise ValueError("Invaled number of interests. Must be [1, 7]")
