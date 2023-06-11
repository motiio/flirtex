from io import BytesIO
from sqlalchemy import delete, select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from src.database.core import DbSession
from src.profile.models import Interest, Profile, ProfilePhoto
from PIL import Image, UnidentifiedImageError

from .schemas import UserProfileCreateRequest, UserProfileReadSchema
from src.s3.core import s3_session
from src.config.core import settings


async def get(
    *,
    db_session: DbSession,
    profile_id: int,
) -> UserProfileReadSchema:
    """Returns a user's profile"""
    q = select(Profile).where(Profile.id == profile_id)  # noqa
    return (await db_session.execute(q)).scalars().first()


async def get_profile_by_user_id(
    *,
    db_session: DbSession,
    user_id: int,
) -> Profile:
    """Returns a user's profile"""
    q = (
        select(Profile)
        .where(Profile.owner_id == user_id)  # noqa
        .options(selectinload(Profile.interests))
    )
    result = (await db_session.execute(q)).scalars().first()
    return result


async def create(
    *,
    db_session: DbSession,
    profile_data: UserProfileCreateRequest,
    owner: int,
) -> Profile:
    """Creates a new profile."""
    profile: Profile = Profile(
        **profile_data.dict(exclude={"interests"}), owner_id=owner
    )
    interest_query = select(Interest).where(Interest.id.in_(profile_data.interests))
    interests = list(await db_session.scalars(interest_query))
    profile.interests = interests
    db_session.add(profile)
    await db_session.commit()
    return profile


async def delete_by_id(
    *,
    db_session: DbSession,
    profile_id: int,
) -> Profile:
    """Creates a new profile."""
    q = delete(Profile).where(Profile.id == profile_id).returning(Profile)  # noqa
    deleted_profile = (await db_session.execute(q)).scalars().first()
    await db_session.commit()
    return deleted_profile


async def delete_profile_by_user_id(
    *,
    db_session: DbSession,
    user_id: int,
) -> Profile:
    """Creates a new profile."""
    q = delete(Profile).where(Profile.owner_id == user_id).returning(Profile)
    deleted_profile = (await db_session.execute(q)).scalars().first()
    await db_session.commit()
    return deleted_profile


async def get_profil_photos_count(
    *,
    db_session: DbSession,
    user_id: int,
) -> int:
    q = (
        select(func.count())
        .select_from(ProfilePhoto)
        .join(Profile)
        .where(Profile.owner_id == user_id)
    )
    return (await db_session.execute(q)).scalars().first() or 0


async def add_profile_photo(
    *, db_session: DbSession, profile_id: int, file_idx: int
) -> ProfilePhoto:
    q = (
        insert(ProfilePhoto)
        .values({"profile": profile_id, "displaying_order": file_idx})
        .returning(ProfilePhoto)
    )
    result = (await db_session.execute(q)).scalars().first()
    await db_session.commit()
    return result


async def upload_photo_to_s3(
    *,
    user_id: int,
    db_session: DbSession,
    file_content: bytes,
    file_idx: int,
) -> ProfilePhoto:
    profile: Profile = await get_profile_by_user_id(
        db_session=db_session,
        user_id=user_id,
    )
    profile_photo = await add_profile_photo(
        db_session=db_session,
        profile_id=profile.id,
        file_idx=file_idx,
    )

    async with s3_session.resource(
        "s3", endpoint_url="https://storage.yandexcloud.net"
    ) as s3:
        bucket = await s3.Bucket(settings.S3_PROFILES_BUCKET_NAME)
        await bucket.upload_fileobj(
            Fileobj=BytesIO(file_content),
            Key=f"{profile.id}/photos/queue/{profile_photo.id}",
        )
    return profile_photo


async def is_image(
    *,
    file_content: bytes,
) -> bool:
    try:
        # check file is image
        image = Image.open(BytesIO(file_content))
        image.verify()

        if image.format and image.format.lower() not in ["jpeg", "png", "gif"]:
            return False

        return True

    except (UnidentifiedImageError, FileNotFoundError):
        return False


CREATION_FOLDERS: tuple = (
    "queue/",  # images that ready to be processed by the neural network
    "approved/",  # approved images that don't contain any objectionable content
    "rejected/",
)


async def create_s3_profile_images_storage(
    *,
    profile_id: int,
):
    async with s3_session.resource(
        "s3", endpoint_url="https://storage.yandexcloud.net"
    ) as s3:
        bucket = await s3.Bucket(settings.S3_PROFILES_BUCKET_NAME)
        for folder in CREATION_FOLDERS:
            await bucket.put_object(Key=f"{profile_id}/photos/{folder}/")


async def delete_s3_profile_images_storage(
    *,
    profile_id: int,
):
    async with s3_session.resource(
        "s3",
        endpoint_url="https://storage.yandexcloud.net",
    ) as s3:
        bucket = await s3.Bucket(settings.S3_PROFILES_BUCKET_NAME)
        await bucket.objects.filter(Prefix=str(profile_id)).delete()
