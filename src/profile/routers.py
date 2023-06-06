from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from src.auth.services import CurrentUser
from src.database.core import DbSession
from src.s3.core import S3Client

from .schemas import InterestReadSchema, UserProfileCreateRequest, UserProfileReadSchema
from .services import (
    create,
    create_profile_interests,
    create_s3_profile_images_storage,
    delete_profile_by_user_id,
    get_profile_by_user_id,
)

profile_router = APIRouter()


@profile_router.post("", status_code=HTTP_201_CREATED, response_model=UserProfileReadSchema)
async def register_profile(
    *,
    user: CurrentUser,
    db_session: DbSession,
    s3_client: S3Client,
    registration_data: UserProfileCreateRequest,
):
    """
    Register a new profile for the current user.

    Args:
    - registration_data: The profile data to register.
    - user: The current user.
    - db_session: The database session.
    - s3_client: The s3 session.

    Returns:
        The newly created profile.
    """
    profile = await get_profile_by_user_id(db_session=db_session, user_id=user)
    if profile:
        return profile

    profile = await create(
        db_session=db_session,
        profile_data=registration_data.dict(exclude={"interests"}),
        owner=user,
    )
    await create_profile_interests(
        db_session=db_session, interests=registration_data.interests, profile_id=profile.id
    )
    await create_s3_profile_images_storage(s3_client=s3_client, profile_id=profile.id)

    return profile


@profile_router.get("", response_model=UserProfileReadSchema)
async def get_my_profile(
    *,
    user: CurrentUser,
    db_session: DbSession,
):
    """
    Get current user's profile.

    Returns:
        The user's profile.

    Raises:
    - HTTPExceptions: **HTTP_404_NOT_FOUND**. If user's profile wos not found
    """
    profile: UserProfileReadSchema = await get_profile_by_user_id(
        db_session=db_session, user_id=int(user)
    )
    if not profile:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={"msg": "User profile not found"},
        )
    return profile


@profile_router.patch("", response_model=UserProfileReadSchema, status_code=HTTP_200_OK)
def update_profile(*, user: CurrentUser, db_session: DbSession):
    ...


@profile_router.delete("", status_code=HTTP_200_OK)
async def delete_profile(*, user: CurrentUser, db_session: DbSession):
    await delete_profile_by_user_id(user_id=user, db_session=db_session)
