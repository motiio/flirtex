from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import Field

from src.v1.schemas import BaseSchema
from src.v1.profile.models import LookingGenderEnum, GenderEnum
from src.v1.profile.schemas.interest import InterestOutSchema

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
