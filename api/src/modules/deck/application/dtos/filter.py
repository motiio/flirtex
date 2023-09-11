from uuid import UUID

from src.core.dtos import BaseDTO
from src.modules.deck.application.utils import enums


class FilterInCreateDTO(BaseDTO):
    profile_id: UUID
    age_from: int
    age_to: int
    max_distance: int
    looking_gender: enums.LookingGenderEnum


class FilterOutDTO(BaseDTO):
    looking_gender: enums.LookingGenderEnum
    age_from: int
    age_to: int
    max_distance: int


class FilterInUpdateDTO(BaseDTO):
    age_from: int | None = None
    age_to: int | None = None
    max_distance: int | None = None
    looking_gender: int | None = None
