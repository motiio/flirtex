from sqlalchemy.sql import func
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select, insert
from tenacity.stop import stop_after_attempt
from urllib3.util import retry

from src.database.core import DbSession
from src.profile.models import Interest, Profile, ProfilePhoto
from PIL import Image, UnidentifiedImageError

from src.s3.core import s3_session
from src.config.core import settings

from src.profile.schemas import ProfileInRegistration
from io import BytesIO
import asyncio
import httpx
from botocore.client import Config
from tenacity import retry, retry_if_exception_type


async def get(
    *,
    db_session: DbSession,
    profile_id: int,
) -> Profile:
    """Returns a user's profile"""
    q = (
        select(Profile)
        .where(Profile.id == profile_id)  # noqa
        .options(
            selectinload(Profile.interests),
            selectinload(Profile.photos),
        )
    )
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
        .options(
            selectinload(Profile.interests),
            selectinload(Profile.photos),
        )
    )
    result = (await db_session.execute(q)).scalars().first()
    return result


# TODO: refactor sql query
async def create(
    *,
    db_session: DbSession,
    profile_data: ProfileInRegistration,
    owner: int,
) -> Profile:
    """Creates a new profile."""
    profile: Profile = Profile(
        **profile_data.dict(exclude={"interests"}), owner_id=owner, photos=set()
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
        .values({"profile_id": profile_id, "displaying_order": file_idx})
        .returning(ProfilePhoto)
    )
    print(q)
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
        endpoint_url=settings.S3_CLOUD_ENDPOINT,
    ) as s3:
        bucket = await s3.Bucket(settings.S3_PROFILES_BUCKET_NAME)
        await bucket.objects.filter(Prefix=str(profile_id)).delete()


async def get_s3_photo_url(*, client, photo) -> str:
    response = await client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.S3_PROFILES_BUCKET_NAME,
            "Key": f"{photo.profile_id}/photos/queue/{photo.id}",
        },
        ExpiresIn=100,
    )
    return response


@retry(retry=retry_if_exception_type(httpx.HTTPStatusError), stop=stop_after_attempt(5))
async def request_short_url(
    *,
    client: httpx.AsyncClient,
    s3_url: str,
):
    response = await client.get(settings.SHORT_URL_RESOURCE, params={"url": s3_url})
    response.raise_for_status()
    return response.text


async def get_profile_photos(
    *,
    profile_id: int,
    db_sesion: DbSession,
):
    profile = await get(db_session=db_sesion, profile_id=profile_id)

    async with s3_session.client(
        "s3",
        endpoint_url=settings.S3_CLOUD_ENDPOINT,
        region_name="ru-central-a",
        config=Config(signature_version="s3v4"),
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    ) as s3_client:
        tasks = [
            get_s3_photo_url(client=s3_client, photo=photo) for photo in profile.photos
        ]
        s3_urls = await asyncio.gather(*tasks)

    async with httpx.AsyncClient() as client:
        tasks = [request_short_url(client=client, s3_url=url) for url in s3_urls]
        photo_urls = await asyncio.gather(*tasks)

    return photo_urls
