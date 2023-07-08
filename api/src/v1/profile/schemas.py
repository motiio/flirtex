from datetime import date
from typing import Optional
from uuid import UUID
from src.v1.photo.schemas import PhotoOutReadSchema


from src.v1.profile.models import GenderEnum, LookingGenderEnum, ProfileInterests
from src.v1.interest.schemas import InterestOutSchema, InterestsOutSchema
from src.v1.base.schemas import BaseSchema

###############################################################
#                         In Schemas                          #
###############################################################


class ProfileInCreateSchema(BaseSchema):
    name: str
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    owner_id: UUID
    bio: str


class ProfileInUpdateSchema(BaseSchema):
    owner_id: UUID
    bio: Optional[str]


class ProfileInReadSchema(BaseSchema):
    owner_id: UUID
    id: UUID


class ProfileInterestsCreateSchema(BaseSchema):
    profile_id: UUID
    interests: list[InterestOutSchema]


###############################################################
#                        Out Schemas                          #
###############################################################


class ProfileOutCreateSchema(BaseSchema):
    name: str
    bio: Optional[str]
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    owner_id: UUID

    class Config:
        from_attributes = True


class ProfileOutReadSchema(BaseSchema):
    id: UUID
    name: str
    bio: Optional[str]
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    interests: Optional[list[InterestOutSchema]] = None
    photos: Optional[list[PhotoOutReadSchema]] = None
    owner_id: UUID

    class Config:
        from_attributes = True
