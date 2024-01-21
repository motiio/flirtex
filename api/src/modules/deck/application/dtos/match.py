from uuid import UUID

from pydantic import AliasChoices, Field, validator

from src.core.dtos import BaseDTO

from src.modules.profile.application.dtos.profile import PhotoOutDTO

class MatchOutDTO:
    profile_1: UUID
    profile_2: UUID


class MatchProfileOutDTO(BaseDTO):
    match_id: UUID
    profile_id: UUID
    name: str = Field(..., alias="profile_name")
    bio: str | None = Field(..., alias="profile_bio")
    photo_url: str | None = Field(..., alias="profile_main_photo_url")
    tg_username: str | None = Field(..., alias="user_tg_username")


class MatchesOutDTO(BaseDTO):
    profiles: list[MatchProfileOutDTO]


class MatchMessageDTO(BaseDTO):
    match_id: UUID
    profile_id: UUID = Field(validation_alias=AliasChoices("profile_id", "id"))
    name: str | None
    bio: str | None
    tg_username: str | None
    photos: list[PhotoOutDTO] | None

    @validator("photos", pre=True)
    def sort_and_get_first_photo(cls, v):
        if v:
            sorted_photos = sorted(v, key=lambda photo: photo.get("displaying_order"))
            return sorted_photos[:1]
        return v
