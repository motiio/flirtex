from typing import TypeVar, Union

from src.core.dtos import BaseDTO, BaseS3DTO
from src.core.entities import BaseEntity
from src.core.models import BaseModel

ENTITY = TypeVar("ENTITY", bound=Union[BaseEntity, BaseDTO, BaseS3DTO])
TABLE = TypeVar("TABLE", bound=Union[BaseModel, BaseDTO, BaseS3DTO])

IN_DTO = TypeVar("IN_DTO", bound=BaseDTO)
OUT_DTO = TypeVar("OUT_DTO", bound=BaseDTO)

IN_S3_DTO = TypeVar("IN_S3_DTO", bound=BaseS3DTO)
OUT_S3_DTO = TypeVar("OUT_S3_DTO", bound=BaseS3DTO)
BUCKET_NAME = TypeVar("BUCKET_NAME", bound=str)
