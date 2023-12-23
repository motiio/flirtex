from uuid import UUID

from src.core.schemas import BaseSchema


class ReadPhotoOutSchema(BaseSchema):
    id: UUID
    displaying_order: int
    url: str
