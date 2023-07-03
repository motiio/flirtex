from datetime import date
from typing import Optional
from uuid import UUID

from src.v1.profile.models import GenderEnum, LookingGenderEnum
from src.v1.profile.schemas.interest import InterestOutSchema
from src.v1.schemas import BaseSchema

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
    name: str
    bio: Optional[str]
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    interests: Optional[list[InterestOutSchema]] = None
    owner_id: UUID

    class Config:
        from_attributes = True
