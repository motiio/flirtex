from fastapi import APIRouter

from src.v1.auth.dependencies.current_user import CurrentUser
from src.v1.config.database import DbSession
from src.v1.profile.dtos import (
    InterestsPutResponse,
    ProfileCreateRequest,
    ProfileUpdateRequest,
    ProfileCreateResponse,
    ProfileReadResponse,
    ProfileInterestsCreateRequest,
)
from src.v1.profile.models import Interest
from src.v1.profile.repositories.interest import InterestReadOnlyRepository
from src.v1.profile.repositories.profile import ProfileRepository
from src.v1.profile.schemas.interest import InterestOutSchema, InterestsOutSchema
from src.v1.profile.schemas.profile import (
    ProfileInCreateSchema,
    ProfileOutCreateSchema,
    ProfileInUpdateSchema,
    ProfileOutReadSchema,
)
from src.v1.profile.usecases.profile import (
    CreateProfile,
    GetUserProfile,
    DeleteUserProfile,
    UpdateUserProfile,
    CreateProfileInterests,
)

profile_router = APIRouter(prefix="/profile")


@profile_router.get(
    "",
    response_model=ProfileReadResponse,
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
    ).execute(
        profile_data=profile_data,
    )
    return ProfileCreateResponse(**profile.model_dump())


@profile_router.patch(
    "",
    response_model=ProfileReadResponse,
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
    ).execute(
        profile_data=profile_data,
    )
    return ProfileReadResponse(**profile.model_dump())


@profile_router.delete(
    "",
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


@profile_router.put("/interests", response_model=InterestsPutResponse)
async def add_profile_interests(
    added_profile_interests: ProfileInterestsCreateRequest,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    interests: list[Interest] = await InterestReadOnlyRepository(
        db_session=db_session
    ).fetch(
        entry_ids=added_profile_interests.interests,
    )

    profile_interests: InterestsOutSchema = await CreateProfileInterests(
        repository=ProfileRepository(db_session=db_session)
    ).execute(interests=interests, owner_id=current_user_id)
    return InterestsPutResponse(**profile_interests.model_dump())
