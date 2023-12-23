from uuid import UUID

from src.core.dtos import BaseDTO


class UpdateTokenInDTO(BaseDTO):
    user: UUID
    user_agent: str
    value: str


class UpdateTokenOutDTO(BaseDTO):
    refresh_token: str
    access_token: str
