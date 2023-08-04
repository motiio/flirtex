from src.core.dtos import BaseDTO
from src.modules.profile.domain.entities import Interest


class InterestsOutDTO(BaseDTO):
    interests: list[Interest]
