from datetime import date, datetime
from uuid import UUID

from dateutil.relativedelta import relativedelta
from pydantic import Field, field_validator

from src.v1.config.schemas import BaseSchema
from src.v1.profile.models import GenderEnum, LookingGenderEnum

###############################################################
#                Request data transfer objects                #
###############################################################


class ProfileRequestCreate(BaseSchema):
    name: str = Field(max_length=32)
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    interests: list[UUID] = Field(max_length=7)

    @field_validator("birthdate")
    def check_legal_age(cls, v):
        difference_in_years = relativedelta(datetime.now(), v).years
        if difference_in_years < 18:
            raise ValueError("Your age must be 18+")
        elif difference_in_years > 120:
            raise ValueError("You're too old, sorry")
        return v


################################################################
#                Response data transfer objects                #
################################################################


class InterestResponse(BaseSchema):
    id: UUID
    name: str
    icon: str


class ProfileResponse(BaseSchema):
    name: str
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    interests: list[InterestResponse]
