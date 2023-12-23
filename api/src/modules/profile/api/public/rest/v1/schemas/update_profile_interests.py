from uuid import UUID

from pydantic import field_validator

from src.core.schemas import BaseSchema


class UpdateProfileInterestsRequestSchema(BaseSchema):
    interests: list[UUID]

    @field_validator("interests")
    def check_interests_len(cls, v):
        if v is None:
            return v

        if 0 < len(v) < 8:
            return v

        raise ValueError("Invaled number of interests. Must be [1, 7]")
