from datetime import date
from uuid import UUID
from src.v1.config.schemas import BaseSchema
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
    interests: list[UUID]
    owner_id: UUID


###############################################################
#                        Out Schemas                          #
###############################################################


class ProfileOutSchema(BaseSchema):
    name: str
    birthdate: date
    looking_gender: LookingGenderEnum
    gender: GenderEnum
    interests: list[InterestOutSchema]
    owner_id: UUID

    class Config:
        from_attributes = True
