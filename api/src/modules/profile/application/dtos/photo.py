from uuid import UUID

from src.core.dtos import BaseDTO, BaseS3DTO


class PhotoInCreateDTO(BaseDTO):
    user_id: UUID
    content: bytes


class PhotoInDeleteDTO(BaseDTO):
    user_id: UUID
    photo_id: UUID


class PhotoOrderDTO(BaseDTO):
    photo_id: UUID
    displaying_order: int


class UpdatePhotosOrderInDTO(BaseDTO):
    user_id: UUID
    photo_orders: list[PhotoOrderDTO]


class UpdatePhotosOrderOutDTO(BaseDTO):
    photos: list[PhotoOrderDTO]


class PhotoInS3UploadDTO(BaseS3DTO):
    key: str
    content: bytes


class PhotoOutDTO(BaseDTO):
    id: UUID
    displaying_order: int
    url: str
