from uuid import UUID
from hashlib import md5
from fastapi import APIRouter, Form, UploadFile, BackgroundTasks
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
)

from src.v1.config.s3 import S3Session
from src.v1.config.database import DbSession
from src.v1.auth.dependencies.user import CurrentUser

from src.v1.config.settings import settings
from src.v1.photo.schemas import (
    PhotoInCreateSchema,
    PhotoInS3CreateSchema,
    PhotoInDeleteSchema,
    PhotoOutCreateSchema,
    PhotoOutDeleteSchema,
)
from src.v1.profile.dtos import (
    InterestsReadResponse,
    InterestsCreateRequest,
    ProfileCreateRequest,
    ProfileCreateResponse,
    ProfileReadResponse,
    ProfileUpdateRequest,
)
from src.v1.profile.models import Interest

from src.v1.interest.repositories.db import InterestReadOnlyRepository
from src.v1.photo.usecases import (
    CreatePhoto,
    DeletePhoto,
    DeletePhotoFromS3,
)
from src.v1.photo.repositories.db import PhotoRepository
from src.v1.photo.repositories.s3 import PhotoS3Repository
from src.v1.profile.repositories.db import ProfileRepository

from src.v1.interest.schemas import InterestsOutSchema
from src.v1.profile.schemas import (
    ProfileInCreateSchema,
    ProfileInUpdateSchema,
    ProfileOutCreateSchema,
    ProfileOutReadSchema,
)
from src.v1.profile.usecases import (
    CreateProfile,
    CreateProfileInterests,
    DeleteUserProfile,
    GetUserProfile,
    UpdateUserProfile,
)

from src.v1.photo.bg_tasks import save_photo_to_s3_and_genereat_short_url

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
    print(profile.photos)

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

    profile: ProfileOutReadSchema = await UpdateUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(profile_data=profile_data)

    return ProfileReadResponse(**profile.model_dump())


@profile_router.delete(
    "",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_profile(
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Update token pair.

    Returns:
        The new user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's refresh token is invalid
    """
    await DeleteUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(profile_owner=current_user_id)


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
    photo: UploadFile,
    db_session: DbSession,
    s3_session: S3Session,
    current_user_id: CurrentUser,
    background_tasks: BackgroundTasks,
    displaying_order: int = Form(...),
):
    profile: ProfileOutReadSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    file_content = await photo.read()
    creating_photo_metadata: PhotoInCreateSchema = PhotoInCreateSchema(
        profile_id=profile.id,
        displaying_order=displaying_order,
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
                bucket_name=settings.S3_PROFILES_BUCKET_NAME,
                s3_session=s3_session,
            )
        ).execute,
        key=deleted_photo_data.s3_key,
    )
