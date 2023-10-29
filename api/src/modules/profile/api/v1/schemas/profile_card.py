from uuid import UUID

from src.core.schemas import BaseSchema
from src.modules.profile.application.dtos import PhotoOutDTO


class ProfileCardResponseSchema(BaseSchema):
    id: UUID
    name: str
    age: int
    photos: list[PhotoOutDTO] | None = None
