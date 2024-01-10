from uuid import UUID

from src.core.dtos import BaseDTO


class SkipMessageDTO(BaseDTO):
    skiped_profile: UUID
