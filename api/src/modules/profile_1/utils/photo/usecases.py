import secrets
from io import BytesIO
from uuid import UUID

from PIL import Image
from pydantic import TypeAdapter

from src.v1.base.exceptions import DoesNotExists
from src.v1.base.usecases import BaseUseCase
from src.v1.config.settings import settings
from src.v1.photo.exceptions import MaxPhotoLimit, PhotoAlreadyExists
from src.v1.photo.repositories.db import PhotoRepository
from src.v1.photo.repositories.s3 import PhotoS3Repository
from src.v1.photo.schemas import (
    PhotoInCreateSchema,
    PhotoInDeleteSchema,
    PhotoInPreprocessSchema,
    PhotoInS3CreateSchema,
    PhotoInUpdateSchema,
    PhotoOutCreateSchema,
    PhotoOutDeleteSchema,
    PhotoOutPreprocessSchema,
    PhotoOutReadSchema,
    PhotoOutS3CreateSchema,
    PhotosOutUpdateDisplayOrderSchema,
)


class CreatePhoto(
    BaseUseCase[
        PhotoRepository,
        PhotoInCreateSchema,
        PhotoOutCreateSchema,
    ]
):
    async def execute(self, *, in_schema: PhotoInCreateSchema) -> PhotoOutCreateSchema:
        async with self.repository as repo:
            current_photos_count: int = await repo.get_profile_photo_count(
                profile_id=in_schema.profile_id
            )
            existent_photo = await repo.get_profile_photo_by_hash(
                profile_id=in_schema.profile_id, hash=in_schema.hash
            )
            if existent_photo:
                raise PhotoAlreadyExists
            if current_photos_count + 1 > settings.MAX_PROFILE_PHOTOS_COUNT:
                raise MaxPhotoLimit
            new_photo = await repo.create(in_schema=in_schema)
            return PhotoOutCreateSchema.model_validate(new_photo)


class SavePhotoToS3(
    BaseUseCase[
        PhotoS3Repository,
        PhotoInS3CreateSchema,
        PhotoOutS3CreateSchema,
    ]
):
    async def execute(self, *, in_schema: PhotoInS3CreateSchema):
        webp_image_bytes = PreprocessImage(repository=None).execute(in_photo_data=in_schema.content)
        in_schema.content = webp_image_bytes
        await self.repository.create(in_schema=in_schema)
        return PhotoOutS3CreateSchema(key=in_schema.key, id=in_schema.id)


class PreprocessImage(
    BaseUseCase[
        None,
        PhotoInPreprocessSchema,
        PhotoOutPreprocessSchema,
    ]
):
    image_data: bytes

    def _resize(self, *, new_height: int, new_width: int, image_data: bytes) -> bytes:
        image = Image.open(BytesIO(image_data))
        resized_image = image.resize((new_width, new_height))
        temp_buffer = BytesIO()
        resized_image.save(temp_buffer, format="JPEG")

        return temp_buffer.getvalue()

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

    def execute(self, *, in_photo_data: bytes):
        resized_image = self._resize(image_data=in_photo_data, new_height=848, new_width=600)
        clear_image_data = self._remove_metadata(image_data=resized_image)
        webp_image = self._convert_to_webp(image_data=clear_image_data)
        return webp_image


class DeletePhoto(
    BaseUseCase[
        PhotoRepository,
        PhotoInDeleteSchema,
        PhotoOutDeleteSchema,
    ]
):
    async def execute(self, *, in_schema: PhotoInDeleteSchema) -> PhotoOutDeleteSchema:
        async with self.repository as repo:
            deleted_photo = await repo.delete(
                photo_id=in_schema.photo_id, profile_id=in_schema.profile_id
            )
            return PhotoOutDeleteSchema.model_validate(deleted_photo)


class DeletePhotoFromS3(
    BaseUseCase[
        PhotoS3Repository,
        PhotoInS3CreateSchema,
        PhotoOutS3CreateSchema,
    ]
):
    async def execute(self, *, key: str):
        try:
            await self.repository.delete(key=key)
        except DoesNotExists:
            pass


class GeneratePresignedUrl(
    BaseUseCase[
        PhotoS3Repository,
        PhotoInS3CreateSchema,
        PhotoOutS3CreateSchema,
    ]
):
    async def execute(self, *, key: str):
        presigned_url = await self.repository.generate_presigned_url(key=key)
        return presigned_url


class GenerateShortUrl(
    BaseUseCase[
        PhotoRepository,
        PhotoInDeleteSchema,
        PhotoOutDeleteSchema,
    ]
):
    async def execute(self, photo_id: UUID, presigned_url):
        url: str = self._generate_unique_string(7)
        async with self.repository as repo:
            await repo.set_short_url(photo_id=photo_id, short_url=url, presigned_url=presigned_url)

    def _generate_unique_string(self, length):
        unique_string = secrets.token_urlsafe(length)[:length]
        return unique_string


class DropS3PhotoStorage(
    BaseUseCase[
        PhotoS3Repository,
        None,
        None,
    ]
):
    async def execute(self, *, profile_id: UUID):
        try:
            await self.repository.delete(key=str(profile_id))
        except DoesNotExists:
            pass


class ChangeDisplayingOrder(
    BaseUseCase[
        PhotoRepository,
        PhotoInUpdateSchema,
        PhotosOutUpdateDisplayOrderSchema,
    ]
):
    async def execute(self, *, in_schema: PhotoInUpdateSchema, profile_id: UUID):
        async with self.repository as repo:
            await repo.update(in_schema=in_schema)

        new_photo_orders = await self.repository.get_profile_photos(profile_id=profile_id)

        return PhotosOutUpdateDisplayOrderSchema(
            photos=TypeAdapter(list[PhotoOutReadSchema]).validate_python(new_photo_orders)
        )
