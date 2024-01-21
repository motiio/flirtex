from typing import Optional
from uuid import UUID
from pydantic import validator

from src.core.dtos import BaseDTO
from src.modules.profile.application.dtos.profile import PhotoOutDTO
from src.modules.profile.application.utils import enums as profile_enums


class LikeOutDTO(BaseDTO):
    id: UUID
    source_profile: UUID
    targe_profile: UUID


class LikeReactionProfileDTO(BaseDTO):
    id: UUID
    name: str
    age: int
    gender: profile_enums.GenderEnum
    photos: Optional[list[PhotoOutDTO]]


class LikeReactionsDTO(BaseDTO):
    profiles: list[LikeReactionProfileDTO]


class LikeMessageDTO(BaseDTO):
    id: UUID
    name: str
    age: int
    gender: profile_enums.GenderEnum
    photos: Optional[list[PhotoOutDTO]]

    @validator("photos", pre=True)
    def sort_and_get_first_photo(cls, v):
        if v:
            sorted_photos = sorted(v, key=lambda photo: photo.get("displaying_order"))
            return sorted_photos[:1]
        return v
