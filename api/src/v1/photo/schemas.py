from hashlib import md5
from typing import Optional
from uuid import UUID

from fastapi import UploadFile

from src.v1.base.schemas import BaseS3Schema, BaseSchema
from pydantic import PrivateAttr, computed_field
from src.v1.config.settings import settings

from src.v1.photo.models import ProcessStatusEnum

###############################################################
#                         In Schemas                          #
###############################################################


class PhotoInReadSchema(BaseSchema):
    id: UUID
    profile_id: UUID
    displaying_order: int


class PhotoInCreateSchema(BaseSchema):
    profile_id: UUID
    displaying_order: int
    status: ProcessStatusEnum = ProcessStatusEnum.processing
    hash: str


class PhotoInUpdateSchema(BaseSchema):
    displaying_order: int


class PhotoInPreprocessSchema(BaseSchema):
    content: bytes


class PhotoInS3CreateSchema(BaseS3Schema):
    id: UUID
    content: bytes


class PhotoInS3UpdateSchema(BaseS3Schema):
    content: bytes


class PhotoInDeleteSchema(BaseSchema):
    profile_id: UUID
    photo_id: UUID


###############################################################
#                        Out Schemas                          #
###############################################################


class PhotoOutCreateSchema(BaseSchema):
    id: UUID
    displaying_order: int
    status: ProcessStatusEnum
    status_description: Optional[str]
    s3_key: Optional[str]

    class Config:
        from_attributes = True


class PhotoOutReadSchema(BaseSchema):
    id: UUID
    profile_id: UUID
    displaying_order: int
    status: ProcessStatusEnum
    status_description: Optional[str]
    short_url: str

    class Config:
        from_attributes = True


class PhotoOutPreprocessSchema(BaseSchema):
    content: bytes


class PhotoOutS3CreateSchema(BaseSchema):
    id: UUID
    s3_key: str


class PhotoOutDeleteSchema(BaseSchema):
    s3_key: str
