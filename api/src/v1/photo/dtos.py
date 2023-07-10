from uuid import UUID

from src.v1.base.schemas import BaseSchema
from src.v1.photo.models import ProcessStatusEnum

###############################################################
#                Request data transfer objects                #
###############################################################

...

################################################################
#                Response data transfer objects                #
################################################################


class PhotoReadResponse(BaseSchema):
    id: UUID
    displaying_order: int
    status: ProcessStatusEnum
    short_url: str
