from hashlib import md5
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
)
from src.v1 import profile

from src.v1.auth.dependencies.user import CurrentUser
from src.v1.config.database import DbSession
from src.v1.config.s3 import S3Session
from src.v1.config.settings import settings
from src.v1.interest.repositories.db import InterestReadOnlyRepository
from src.v1.interest.schemas import InterestsOutSchema
from src.v1.photo.bg_tasks import save_photo_to_s3_and_genereat_short_url
from src.v1.photo.dependencies.validate_photo import (
    ValidImageFile,
)
from src.v1.photo.repositories.db import PhotoRepository
from src.v1.photo.repositories.s3 import PhotoS3Repository
from src.v1.photo.schemas import (
    PhotoInCreateSchema,
    PhotoInDeleteSchema,
    PhotoInS3CreateSchema,
    PhotoInUpdateSchema,
    PhotoOutCreateSchema,
    PhotoOutDeleteSchema,
    PhotosOutUpdateDisplayOrderSchema,
)
from src.v1.photo.usecases import (
    ChangeDisplayingOrder,
    CreatePhoto,
    DeletePhoto,
    DeletePhotoFromS3,
    DropS3PhotoStorage,
)
from src.v1.profile.dtos import (
    InterestsCreateRequest,
    InterestsReadResponse,
    PhotoOrderChangeRequest,
    PhotosOrderChangeResponse,
    ProfileCreateRequest,
    ProfileCreateResponse,
    ProfileLocationCreateRequest,
    ProfileReadResponse,
    ProfileUpdateRequest,
)
from src.v1.profile.models import Interest
from src.v1.profile.repositories.db import ProfileRepository
from src.v1.profile.schemas import (
    ProfileInCreateSchema,
    ProfileInUpdateSchema,
    ProfileOutCreateSchema,
    ProfileOutReadSchema,
)
from src.v1.profile.usecases import (
    CreateProfile,
    CreateProfileInterests,
    DeleteProfile,
    GetUserProfile,
    UpdateProfile,
)
from src.v1.profile.utils.geo.models import Point

profile_router = APIRouter(prefix="/profile")


@profile_router.get(
    "",
    response_model=ProfileReadResponse,
    status_code=HTTP_200_OK,
)
async def get_curret_user_profile(
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Get users's Profile.

    Returns:
        The user's **Profile**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access is invalid
    """
    profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    return ProfileReadResponse(**profile.model_dump())


@profile_router.post(
    "",
    response_model=ProfileCreateResponse,
    status_code=HTTP_201_CREATED,
)
async def create_profile(
    registration_data: ProfileCreateRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Registrate users's Profile.

    Returns:
        The user's **Profile**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access is invalid
    """
    profile_data: ProfileInCreateSchema = ProfileInCreateSchema(
        **registration_data.model_dump(),
        owner_id=current_user_id,
    )

    profile: ProfileOutCreateSchema = await CreateProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(profile_data=profile_data)

    return ProfileCreateResponse(**profile.model_dump())


@profile_router.patch(
    "",
    response_model=ProfileReadResponse,
    status_code=HTTP_200_OK,
)
async def update_profile(
    profile_data_to_update: ProfileUpdateRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Registrate users's Profile.

    Returns:
        The user's **Profile**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access is invalid
    """

    profile_data: ProfileInUpdateSchema = ProfileInUpdateSchema(
        **profile_data_to_update.model_dump(),
        owner_id=current_user_id,
    )

    profile: ProfileOutReadSchema = await UpdateProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(profile_data=profile_data)

    return ProfileReadResponse(**profile.model_dump())


@profile_router.delete(
    "",
    status_code=HTTP_202_ACCEPTED,
)
async def delete_profile(
    current_user_id: CurrentUser,
    db_session: DbSession,
    s3_session: S3Session,
    background_tasks: BackgroundTasks,
):
    """
    Update token pair.

    Returns:
        The new user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's refresh token is invalid
    """
    profile = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    await DeleteProfile(
        repository=ProfileRepository(db_session=db_session),
    ).execute(profile_id=profile.id)

    background_tasks.add_task(
        DropS3PhotoStorage(
            repository=PhotoS3Repository(
                s3_session=s3_session,
                bucket_name=settings.S3_PHOTO_BUCKET_NAME,
            )
        ).execute,
        profile_id=profile.id,
    )


@profile_router.put(
    "/interests",
    response_model=InterestsReadResponse,
    status_code=HTTP_201_CREATED,
)
async def add_profile_interests(
    added_profile_interests: InterestsCreateRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Put profile interests.

    Returns:
        The new profile **interests**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's refresh token is invalid
    """
    interests: list[Interest] = await InterestReadOnlyRepository(
        db_session=db_session
    ).fetch(entry_ids=added_profile_interests.interests)

    profile_interests: InterestsOutSchema = await CreateProfileInterests(
        repository=ProfileRepository(db_session=db_session)
    ).execute(
        interests=interests,
        owner_id=current_user_id,
    )

    return InterestsReadResponse(**profile_interests.model_dump())


@profile_router.post(
    "/photo",
    status_code=HTTP_202_ACCEPTED,
)
async def add_profile_photo(
    photo: ValidImageFile,
    db_session: DbSession,
    s3_session: S3Session,
    current_user_id: CurrentUser,
    background_tasks: BackgroundTasks,
):
    profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    file_content = await photo.read()

    creating_photo_metadata: PhotoInCreateSchema = PhotoInCreateSchema(
        profile_id=profile.id,
        hash=md5(file_content).hexdigest(),
    )

    photo_data: PhotoOutCreateSchema = await CreatePhoto(
        repository=PhotoRepository(db_session=db_session)
    ).execute(in_schema=creating_photo_metadata)

    photo_data_to_s3: PhotoInS3CreateSchema = PhotoInS3CreateSchema(
        id=photo_data.id,
        key=f"{profile.id}/{photo_data.id}.webp",
        content=file_content,
    )
    background_tasks.add_task(
        func=save_photo_to_s3_and_genereat_short_url,
        in_schema=photo_data_to_s3,
        s3_session=s3_session,
        db_session=db_session,
    )


@profile_router.delete(
    "/photo/{photo_id}",
    status_code=HTTP_202_ACCEPTED,
)
async def delete_photo(
    photo_id: UUID,
    db_session: DbSession,
    s3_session: S3Session,
    current_user_id: CurrentUser,
    background_tasks: BackgroundTasks,
):
    current_profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    photo_data_to_delete: PhotoInDeleteSchema = PhotoInDeleteSchema(
        profile_id=current_profile.id,
        photo_id=photo_id,
    )

    deleted_photo_data: PhotoOutDeleteSchema = await DeletePhoto(
        repository=PhotoRepository(db_session=db_session)
    ).execute(in_schema=photo_data_to_delete)

    background_tasks.add_task(
        DeletePhotoFromS3(
            repository=PhotoS3Repository(
                bucket_name=settings.S3_PHOTO_BUCKET_NAME,
                s3_session=s3_session,
            )
        ).execute,
        key=f"{deleted_photo_data.profile_id}/{deleted_photo_data.id}.webp",
    )


@profile_router.patch("/photo")
async def update_photo_order(
    photo_order_change_object: PhotoOrderChangeRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    current_profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    changing_display_order_data = PhotoInUpdateSchema(
        id=photo_order_change_object.id,
        displaying_order=photo_order_change_object.displaying_order,
    )

    new_ordered_photos: PhotosOutUpdateDisplayOrderSchema = await ChangeDisplayingOrder(
        repository=PhotoRepository(db_session=db_session)
    ).execute(profile_id=current_profile.id, in_schema=changing_display_order_data)

    return PhotosOrderChangeResponse(**new_ordered_photos.model_dump())


@profile_router.post("/location")
async def create_position(
    location: ProfileLocationCreateRequest,
):
    return location
