from typing import TypeVar, Union

from src.core.dtos import BaseDTO
from src.core.entities import BaseEntity
from src.core.models import BaseModel

ENTITY = TypeVar("ENTITY", bound=BaseEntity)
TABLE = TypeVar("TABLE", bound=BaseModel)

IN_DTO = TypeVar("IN_DTO", bound=Union[BaseDTO, None])
OUT_DTO = TypeVar("OUT_DTO", bound=Union[BaseDTO, None])
