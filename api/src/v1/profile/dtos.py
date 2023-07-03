from datetime import date, datetime
from typing import Optional
from uuid import UUID

from dateutil.relativedelta import relativedelta
from pydantic import Field, field_validator

from src.v1.profile.models import GenderEnum, LookingGenderEnum
from src.v1.schemas import BaseSchema

###############################################################
#                Request data transfer objects                #
###############################################################


class ProfileCreateRequest(BaseSchema):
    name: str = Field(max_length=32)
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    bio: Optional[str] = Field("", max_length=600)

    @field_validator("birthdate")
    def check_legal_age(cls, v):
        difference_in_years = relativedelta(datetime.now(), v).years
        if difference_in_years < 18:
            raise ValueError("Your age must be 18+")
        elif difference_in_years > 120:
            raise ValueError("You're too old, sorry")
        return v


class ProfileUpdateRequest(BaseSchema):
    bio: str = Field("", max_length=600)


class ProfileInterestsCreateRequest(BaseSchema):
    interests: list[UUID] = Field(max_length=7)


################################################################
#                Response data transfer objects                #
################################################################


class InterestReadResponse(BaseSchema):
    id: UUID
    name: str
    icon: str


class InterestsReadResponse(BaseSchema):
    interests: list[InterestReadResponse]


class ProfileCreateResponse(BaseSchema):
    name: str
    bio: str
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum


class ProfileReadResponse(BaseSchema):
    name: str
    bio: str
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    interests: list[InterestReadResponse]
