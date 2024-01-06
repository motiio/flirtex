from uuid import UUID

from src.core.schemas import BaseSchema
from src.core.types import Pagination


class MatchOutSchema(BaseSchema):
    match_id: UUID
    profile_id: UUID
    name: str
    bio: str | None
    photo_url: str | None


class MatchesOutSchema(BaseSchema):
    pagination: Pagination
    profiles: list[MatchOutSchema]
