from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.profile.application.dtos.profile import ProfileOutDTO
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.application.repositories.photo import IProfilePhotoS3Repository
from src.modules.profile.domain.exceptions import ProfileNotFound


class DeleteProfileUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
        photo_s3_repo: IProfilePhotoS3Repository,
    ):
        self._profile_repo: IProfileRepository = profile_repository
        self._photo_s3_repo: IProfilePhotoS3Repository = photo_s3_repo

    async def execute(self, owner_id: UUID) -> ProfileOutDTO:
        async with self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=owner_id)
            if not existent_profile:
                raise ProfileNotFound

            deleted_profile = await self._profile_repo.delete(
                entity_id=existent_profile.id
            )
            await self._photo_s3_repo.delete(key=str(existent_profile.id))

            return ProfileOutDTO(**deleted_profile.model_dump())
