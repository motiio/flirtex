from uuid import UUID

from pydantic import Field, field_validator

import src.modules.profile.api.shared as shared
from src.core.schemas import BaseSchema


class UpdateProfileRequestSchema(BaseSchema):
    bio: str | None = Field("", max_length=600)
    interests: list[UUID] | None = None
    location: shared.DistortedPointSchema | None = None

    @field_validator("interests")
    def check_interests_len(cls, v):
        if v is None:
            return v

        if 0 < len(v) < 8:
            return v

        raise ValueError("Invaled number of interests. Must be [1, 7]")
