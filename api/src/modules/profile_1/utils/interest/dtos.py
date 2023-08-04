from uuid import UUID

from src.v1.base.schemas import BaseSchema

###############################################################
#                Request data transfer objects                #
###############################################################

...

################################################################
#                Response data transfer objects                #
################################################################


class InterestResponse(BaseSchema):
    id: UUID
    name: str
    icon: str


class InterestsResponse(BaseSchema):
    interests: list[InterestResponse]
