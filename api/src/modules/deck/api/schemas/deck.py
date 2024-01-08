from uuid import UUID

from src.core.dtos import BaseDTO
from src.modules.profile.application.dtos.interest import InterestOutDTO
from src.modules.profile.application.dtos.photo import PhotoOutDTO
from src.modules.profile.application.utils import enums as profile_enums


class DeckProfileOutResponse(BaseDTO):
    id: UUID
    name: str
    bio: str | None
    age: int
    gender: profile_enums.GenderEnum
    interests: list[InterestOutDTO] | None = None
    photos: list[PhotoOutDTO] | None = None
    distance: int | None = None


class DeckBatchOutResponse(BaseDTO):
    batch: list[DeckProfileOutResponse]
