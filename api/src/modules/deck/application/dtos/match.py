from uuid import UUID

from src.core.dtos import BaseDTO


class MatchOutDTO(BaseDTO):
    profile_1: UUID
    profile_2: UUID
