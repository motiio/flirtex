from datetime import date, datetime
from typing import Optional
from uuid import UUID

from dateutil.relativedelta import relativedelta
from fastapi import File, UploadFile
from pydantic import Field, field_validator

from src.v1.base.schemas import BaseSchema
from src.v1.config.settings import settings
from src.v1.photo.dtos import PhotoReadResponse
from src.v1.photo.schemas import PhotoInUpdateSchema
from src.v1.profile.models import GenderEnum, LookingGenderEnum
from src.v1.profile.utils.geo.models import Point

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
        elif difference_in_years > 100:
            raise ValueError("You're too old, sorry")
        return v


class ProfileUpdateRequest(BaseSchema):
    bio: str = Field("", max_length=600)


class InterestsCreateRequest(BaseSchema):
    interests: list[UUID] = Field(max_length=7)


class PhotoCreateRequest(BaseSchema):
    file: UploadFile = File(...)


class PhotosOrderChangeRequest(BaseSchema):
    photos: list[PhotoInUpdateSchema]

    @field_validator("photos")
    def check_displaying_order_value(cls, v):
        if 1 <= v <= settings.MAX_PROFILE_PHOTOS_COUNT:
            return v
        raise ValueError(f"Value should be between 1 and {settings.MAX_PROFILE_PHOTOS_COUNT}")


class ProfileLocationCreateRequest(BaseSchema):
    point: Point


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
    photos: list[PhotoReadResponse]


class PhotoOrderChangeResponse(BaseSchema):
    id: UUID
    displaying_order: int


class PhotosOrderChangeResponse(BaseSchema):
    photos: list[PhotoOrderChangeResponse]
