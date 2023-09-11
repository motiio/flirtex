from datetime import date
from typing import Optional
from uuid import UUID

import src.modules.profile.domain.entities.types as types
from src.core.dtos import BaseDTO
from src.modules.deck.application.utils import enums as deck_enums
from src.modules.profile.application.dtos.interest import InterestOutDTO
from src.modules.profile.application.dtos.photo import PhotoOutDTO
from src.modules.profile.application.utils import enums as profile_enums


class CreateProfileInDTO(BaseDTO):
    owner_id: UUID
    name: str
    bio: str
    birthdate: date
    gender: profile_enums.GenderEnum
    looking_gender: deck_enums.LookingGenderEnum
    interests: list[UUID] | None = None
    location: types.Location | None


class UpdateProfileInDTO(BaseDTO):
    owner_id: UUID
    bio: str | None = None
    interests: list[UUID] | None = None
    location: types.Location | None = None


class ProfileOutDTO(BaseDTO):
    id: UUID
    name: str
    bio: str
    age: int
    gender: profile_enums.GenderEnum
    interests: Optional[list[InterestOutDTO]]
    photos: Optional[list[PhotoOutDTO]]
    distance: Optional[float] = None
