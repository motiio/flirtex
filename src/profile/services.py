import imghdr
import io

from fastapi import UploadFile
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload

from src.common.schemas import InterestReadSchema
from src.config.core import settings
from src.database.core import DbSession
from src.profile.models import Interest, Profile, ProfileInterests
from src.s3.core import S3Client

from .exception import ImageSizeTooBig, InvalidImageType
from .schemas import UserProfileReadSchema


async def get(*, db_session: DbSession, profile_id: int) -> UserProfileReadSchema:
    """Returns a user's profile"""
    q = select(Profile).where(Profile.id == profile_id)  # noqa
    return (await db_session.execute(q)).scalars().first()


async def get_profile_by_user_id(*, db_session: DbSession, user_id: int) -> UserProfileReadSchema:
    """Returns a user's profile"""
    q = (
        select(Profile)
        .where(Profile.owner == user_id, Profile.is_active == True)  # noqa
        .options(selectinload(Profile.interests))
    )
    result = (await db_session.execute(q)).scalars().first()
    return result


async def create(
    *, db_session: DbSession, profile_data: dict, owner: int
) -> UserProfileReadSchema | None:
    """Creates a new profile."""
    q = insert(Profile).values(**profile_data, owner=owner, is_active=True).returning(Profile)
    result = (await db_session.execute(q)).scalars().first()
    await db_session.commit()
    return result


async def update(*, db_session: DbSession, profile_data: dict) -> UserProfileReadSchema:
    """Update a new profile."""
    ...


async def delete_by_id(*, db_session: DbSession, profile_id: int) -> None:
    """Creates a new profile."""
    q = delete(Profile).where(Profile.id == profile_id)  # noqa
    await db_session.execute(q)
    await db_session.commit()


async def create_profile_interests(*, db_session: DbSession, profile_id: int, interests: list[int]):
    q = select(Interest.id).where(Interest.id.in_(interests))
    existing_interests = (await db_session.execute(q)).scalars().all()

    await db_session.execute(
        insert(ProfileInterests),
        [
            {"profile_id": profile_id, "interest_id": int(interest_id)}
            for interest_id in existing_interests
        ],
    )
    await db_session.commit()


async def delete_profile_by_user_id(*, db_session: DbSession, user_id: int) -> None:
    """Creates a new profile."""
    q = delete(Profile).where(Profile.owner == user_id)  # noqa
    await db_session.execute(q)
    await db_session.commit()


async def create_s3_profile_images_storage(*, profile_id: int, s3_client: S3Client):
    folders = (
        "queue/",  # images that ready to be processed by the neural network
        "approved/",  # approved images that don't contain any objectionable content
        "rejected/",
    )
    for folder in folders:
        await s3_client.put_object(
            Bucket=settings.S3_PROFILES_BUCKET_NAME, Key=f"{profile_id}/profile/images/{folder}"
        )


async def _check_is_image(file: bytes) -> None | bytes:
    ALLOWED_IMAGE_TYPES = ["jpeg", "png", "gif"]
    file_type = imghdr.what(None, h=file)
    if not file_type or file_type not in ALLOWED_IMAGE_TYPES:
        raise InvalidImageType(
            msg=f"Invalid image type. Type must be {ALLOWED_IMAGE_TYPES}", loc="profile_photos"
        )
    return file


async def _check_image_size(*, photo: UploadFile) -> int:
    actual_size = photo.file.seek(0, 2)
    photo.file.seek(0)
    if actual_size > settings.MAX_PROFILE_PHOTO_SIZE_B:
        raise ImageSizeTooBig(
            msg=f"Image size too big. Max size is f{settings.MAX_FILE_SIZE_B} bytes",
            loc="profile_photos",
        )


async def check_profile_photos(*, profile_photos: list[UploadFile]) -> tuple[list, list]:
    checked_images = []
    rejected: list[dict] = []
    for photo in profile_photos:
        try:
            _ = await _check_is_image(await photo.read())
            _ = await _check_image_size(photo=photo)
        except (InvalidImageType, ImageSizeTooBig) as e:
            rejected.append({photo.filename: str(e)})
        else:
            checked_images.append(photo)
    return checked_images, rejected


async def save_profile_photos(
    *, profile_id: int, s3_client: S3Client, checked_photos: list[UploadFile]
):
    file_path = f"{profile_id}/profile/images/queue"
    for idx, photo in enumerate(checked_photos):
        try:
            byte_stream = io.BytesIO(await photo.read())
            await s3_client.upload_fileobj(
                Fileobj=byte_stream,
                Bucket=settings.S3_PROFILES_BUCKET_NAME,
                Key=f"{file_path}/{idx}",
            )
        except Exception as e:
            print(f"Произошла ошибка при загрузке файла в s3: {e}")
