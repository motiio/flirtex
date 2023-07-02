from uuid import UUID

from src.v1.config.schemas import BaseSchema

###############################################################
#                         In Schemas                          #
###############################################################


class InterestInReadSchema(BaseSchema):
    id: UUID


###############################################################
#                        Out Schemas                          #
###############################################################


class InterestOutSchema(BaseSchema):
    id: UUID
    name: str
    icon: str

    class Config:
        from_attributes = True
