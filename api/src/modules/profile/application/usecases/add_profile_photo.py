from hashlib import md5
from io import BytesIO

from PIL import Image

from src.config.settings import settings
from src.core.usecases import IUseCase
from src.modules.profile.application.dtos.photo import (
    PhotoInCreateDTO,
    PhotoInS3UploadDTO,
    PhotoOutDTO,
)
from src.modules.profile.application.repositories import (
    IProfilePhotoRepository,
    IProfilePhotoS3Repository,
    IProfileRepository,
)
from src.modules.profile.domain.entities import ProfilePhoto
from src.modules.profile.domain.exceptions import (
    PhotoAlreadyExists,
    PhotosLimit,
    ProfileNotFound,
)


class AddProfilePhotoUsecase(IUseCase):
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

    async def execute(self, in_dto: PhotoInCreateDTO) -> PhotoOutDTO:
        async with self._photo_repo, self._photo_s3_repo, self._profile_repo:
            profile = await self._profile_repo.get_by_owner(owner_id=in_dto.user_id)

            if not profile:
                raise ProfileNotFound

            photo_numbers = await self._photo_repo.photos_count(profile_id=profile.id)

            if photo_numbers + 1 > settings.MAX_PROFILE_PHOTOS_COUNT:
                raise PhotosLimit

            max_displayin_num = await self._photo_repo.max_displaying_num(
                profile_id=profile.id
            )

            photo = ProfilePhoto.create(
                **in_dto.model_dump(),
                profile_id=profile.id,
                hash=md5(in_dto.content).hexdigest(),
                displaying_order=max_displayin_num + 1,
            )
            if await self._photo_repo.get_by_hash(
                profile_id=profile.id,
                hash=photo.hash,
            ):
                raise PhotoAlreadyExists

            await self._photo_repo.create(in_entity=photo)

            clear_image_data = self._remove_metadata(image_data=in_dto.content)
            webp_image = self._convert_to_webp(image_data=clear_image_data)

            await self._photo_s3_repo.create(
                in_dto=PhotoInS3UploadDTO(
                    key=photo.url,
                    content=webp_image,
                )
            )

            return PhotoOutDTO(**photo.model_dump())

    def _remove_metadata(self, *, image_data: bytes) -> bytes:
        image = Image.open(BytesIO(image_data))
        temp_buffer = BytesIO()
        image.save(temp_buffer, format="JPEG", exif=b"")
        return temp_buffer.getvalue()

    def _convert_to_webp(self, *, image_data: bytes) -> bytes:
        image = Image.open(BytesIO(image_data))
        temp_buffer = BytesIO()
        image.save(temp_buffer, format="WEBP", optimize=True, quality=60)
        return temp_buffer.getvalue()
