from src.core.usecases import IUseCase
from src.modules.profile.application.dtos import (
    PhotoInDeleteDTO,
)
from src.modules.profile.application.repositories import (
    IProfilePhotoRepository,
    IProfilePhotoS3Repository,
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import (
    PhotosLimit,
    ProfileNotFound,
)


class DeleteProfilePhotoUsecase(IUseCase):
    def __init__(
        self,
        *,
        photo_repository: IProfilePhotoRepository,
        profile_repository: IProfileRepository,
        photo_s3_repository: IProfilePhotoS3Repository,
    ):
        self._photo_repo: IProfilePhotoRepository = photo_repository
        self._profile_repo: IProfileRepository = profile_repository
        self._photo_s3_repo: IProfilePhotoS3Repository = photo_s3_repository

    async def execute(self, in_dto: PhotoInDeleteDTO):
        async with self._photo_repo, self._photo_s3_repo, self._profile_repo:
            profile = await self._profile_repo.get_by_owner(owner_id=in_dto.user_id)

            if not profile:
                raise ProfileNotFound

            deleted_photo = await self._photo_repo.get(
                entity_id=in_dto.photo_id, profile_id=profile.id
            )
            if not deleted_photo:
                return

            photo_numbers = await self._photo_repo.photos_count(profile_id=profile.id)

            if photo_numbers <= 1:
                raise PhotosLimit

            deleted_photo = await self._photo_repo.delete(
                entity_id=in_dto.photo_id, profile_id=profile.id
            )

            await self._photo_s3_repo.delete(key=deleted_photo.url)
