from uuid import UUID

from src.v1.base.schemas import BaseSchema

###############################################################
#                         In Schemas                          #
###############################################################


class LikeInCreateSchema(BaseSchema):
    source_profile: UUID
    target_profile: UUID


class SkipInCreateSchema(BaseSchema):
    source_profile: UUID
    target_profile: UUID


class SaveInCreateSchema(BaseSchema):
    source_profile: UUID
    target_profile: UUID


class MatchInCreateSchema(BaseSchema):
    profile_1: UUID
    profile_2: UUID


###############################################################
#                        Out Schemas                          #
###############################################################


class InterestOutSchema(BaseSchema):
    id: UUID
    name: str
    icon: str

    class Config:
        from_attributes = True


class InterestsOutSchema(BaseSchema):
    interests: list[InterestOutSchema]
