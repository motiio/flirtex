from datetime import date
from uuid import UUID

import src.modules.profile.domain.entities.types as types
from src.core.dtos import BaseDTO
from src.modules.profile.application.dtos.interest import InterestOutDTO
from src.modules.profile.application.dtos.photo import PhotoOutDTO
from src.modules.profile.application.utils import enums as profile_enums


class CreateProfileInDTO(BaseDTO):
    owner_id: UUID
    name: str
    birthdate: date
    gender: profile_enums.GenderEnum


class UpdateProfileInDTO(BaseDTO):
    owner_id: UUID
    bio: str | None = None
    interests: list[UUID] | None = None
    location: types.Location | None = None


class UpdateProfileOutDTO(BaseDTO):
    id: UUID
    name: str
    bio: str | None
    age: int
    gender: profile_enums.GenderEnum
    interests: list[InterestOutDTO] | None
    photos: list[PhotoOutDTO] | None
    is_location: bool


class ProfileOutDTO(BaseDTO):
    id: UUID
    name: str
    bio: str | None
    age: int
    gender: profile_enums.GenderEnum
    interests: list[InterestOutDTO] | None
    photos: list[PhotoOutDTO] | None
    distance: float | None = None
