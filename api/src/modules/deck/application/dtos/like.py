from typing import Optional
from uuid import UUID

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
