from typing import Optional
from uuid import UUID

from src.core.schemas import BaseSchema
from src.core.types import Pagination
from src.modules.profile.application.dtos.profile import PhotoOutDTO
from src.modules.profile.application.utils import enums as profile_enums


class LikeReactionProfileOutSchema(BaseSchema):
    id: UUID
    name: str
    age: int
    gender: profile_enums.GenderEnum
    photos: Optional[list[PhotoOutDTO]]


class LikeReactionsOutSchema(BaseSchema):
    pagination: Pagination
    profiles: list[LikeReactionProfileOutSchema]
