from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.entities import BaseEntity
from src.modules.profile.application.utils.enums import PhotoProcessStatusEnum


@dataclass
class PhotoDAE(BaseEntity):
    id: UUID
    profile_id: UUID
    displaying_order: int
    status: PhotoProcessStatusEnum
    status_description: str
    hash: str
    url: str

    def __init__(
        self,
        id: UUID,
        profile_id: UUID,
        displaying_order: int,
        status: PhotoProcessStatusEnum,
        status_description: str,
        hash: str,
        url: str,
    ):
        self.id = id
        self.profile_id = profile_id
        self.displaying_order = displaying_order
        self.status = status
        self.status_description = status_description
        self.hash = hash
        self.url = url

    @classmethod
    def create(
        cls,
        *,
        id=None,
        profile_id,
        displaying_order,
        hash,
        url=None,
        status=PhotoProcessStatusEnum.processing,
        status_description="",
        **kwargs,
    ):
        if id is None:
            id = uuid4()

        if url is None:
            url = f"{profile_id}/photo/{id}.webp"

        photo = PhotoDAE(
            id=id,
            profile_id=profile_id,
            displaying_order=displaying_order,
            status=status,
            status_description=status_description,
            hash=hash,
            url=url,
        )
        return photo

    def set_displaying_order(self, value: int):
        self.displaying_order = value
