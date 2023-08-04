from uuid import UUID

from src.v1.base.schemas import BaseSchema


###############################################################
#                Request data transfer objects                #
###############################################################
class LikeRequest(BaseSchema):
    profile: UUID


class SkipRequest(BaseSchema):
    profile: UUID


class SaveRequest(BaseSchema):
    profile: UUID


################################################################
#                Response data transfer objects                #
################################################################
...
