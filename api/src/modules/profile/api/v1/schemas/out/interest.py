from uuid import UUID

from src.core.schemas import BaseSchema


class ReadInterestOutSchema(BaseSchema):
    id: UUID
    name: str
    icon: str
