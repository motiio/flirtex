from typing import Any
from uuid import UUID

from pydantic import model_validator

from src.core.schemas import BaseSchema
from src.modules.profile.api.public.rest.v1.schemas.out.interest import (
    ReadInterestOutSchema,
)
from src.modules.profile.application.utils import enums as profile_enums

from .photo import ReadPhotoOutSchema


class ReadMyProfileOutSchema(BaseSchema):
    id: UUID
    name: str
    age: int
    gender: profile_enums.GenderEnum
    bio: str | None
    interests: list[ReadInterestOutSchema] | None
    photos: list[ReadPhotoOutSchema] | None

    # calculated fields
    has_location: bool

    @model_validator(mode="before")
    def pre_root(cls, values: dict[str, Any]) -> dict[str, Any]:
        has_location = True if values.get("location") else False
        values = values | {"has_location": has_location}
        return values


class ReadProfileOutSchema(BaseSchema):
    id: UUID
    name: str
    age: int
    gender: profile_enums.GenderEnum
    bio: str | None
    interests: list[ReadInterestOutSchema] | None
    photos: list[ReadPhotoOutSchema] | None

    distance: float | None = None
