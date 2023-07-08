from datetime import date, datetime
from re import L
from typing import Optional
from uuid import UUID

from dateutil.relativedelta import relativedelta
from fastapi import File, UploadFile
from pydantic import Field, field_validator
from src.v1.photo.models import ProcessStatusEnum

from src.v1.profile.models import GenderEnum, LookingGenderEnum
from src.v1.base.schemas import BaseSchema

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
