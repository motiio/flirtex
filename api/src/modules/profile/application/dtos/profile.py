from datetime import date
from typing import Optional
from uuid import UUID

from src.core.dtos import BaseDTO
from src.modules.profile.application.dtos.interest import InterestOutDTO
from src.modules.profile.application.dtos.photo import PhotoOutDTO
from src.modules.profile.application.utils.enums import GenderEnum, LookingGenderEnum


class CreateProfileInDTO(BaseDTO):
    owner_id: UUID
    name: str
    bio: str
    birthdate: date
    gender: GenderEnum
    looking_gender: LookingGenderEnum
    interests: list[UUID] | None = None


class UpdateProfileInDTO(BaseDTO):
    owner_id: UUID
    bio: str | None = None
    interests: list[UUID] | None = None


class ProfileOutDTO(BaseDTO):
    name: str
    bio: str
    birthdate: date
    gender: GenderEnum
    looking_gender: LookingGenderEnum
    interests: Optional[list[InterestOutDTO]]
    photos: Optional[list[PhotoOutDTO]]
