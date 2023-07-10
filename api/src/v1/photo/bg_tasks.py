from src.v1.config.database import DbSession
from src.v1.config.s3 import S3Session
from src.v1.config.settings import settings
from src.v1.photo.repositories.db import PhotoRepository
from src.v1.photo.repositories.s3 import PhotoS3Repository
from src.v1.photo.schemas import PhotoInS3CreateSchema, PhotoOutS3CreateSchema
from src.v1.photo.usecases import GeneratePresignedUrl, GenerateShortUrl, SavePhotoToS3


async def save_photo_to_s3_and_genereat_short_url(
    *, in_schema: PhotoInS3CreateSchema, s3_session: S3Session, db_session: DbSession
):
    photo: PhotoOutS3CreateSchema = await SavePhotoToS3(
        repository=PhotoS3Repository(
            bucket_name=settings.S3_PHOTO_BUCKET_NAME, s3_session=s3_session
        )
    ).execute(in_schema=in_schema)

    presigned_url: str = await GeneratePresignedUrl(
        repository=PhotoS3Repository(
            bucket_name=settings.S3_PHOTO_BUCKET_NAME, s3_session=s3_session
        )
    ).execute(key=photo.key)

    await GenerateShortUrl(repository=PhotoRepository(db_session=db_session)).execute(
        photo_id=photo.id, presigned_url=presigned_url
    )
