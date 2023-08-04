from uuid import UUID

from src.core.dtos import BaseDTO


class InterestOutDTO(BaseDTO):
    id: UUID
    name: str
    icon: str
