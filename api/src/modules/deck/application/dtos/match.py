from uuid import UUID

from pydantic import Field

from src.core.dtos import BaseDTO


class MatchOutDTO:
    profile_1: UUID
    profile_2: UUID


class MatchProfileOutDTO(BaseDTO):
    match_id: UUID
    profile_id: UUID
    name: str = Field(..., alias="profile_name")
    bio: str | None = Field(..., alias="profile_bio")
    photo_url: str | None = Field(..., alias="profile_main_photo_url")


class MatchesOutDTO(BaseDTO):
    profiles: list[MatchProfileOutDTO]
