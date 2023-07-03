from typing import Optional
from fastapi import APIRouter

from src.v1.auth.dependencies.current_user import CurrentUser
from src.v1.config.database import DbSession
from src.v1.profile.dtos import (
    ProfileRequestCreate,
    ProfileRequestUpdate,
    ProfileResponse,
)
from src.v1.profile.models import Interest
from src.v1.profile.repositories.interest import InterestReadOnlyRepository
from src.v1.profile.repositories.profile import ProfileRepository
from src.v1.profile.schemas.profile import (
    ProfileInCreateSchema,
    ProfileInUpdateSchema,
    ProfileOutSchema,
)
from src.v1.profile.usecases.profile import (
    GetOrCreateProfile,
    GetUserProfile,
    DeleteUserProfile,
    UpdateUserProfile,
)

profile_router = APIRouter(prefix="/profile")


@profile_router.get(
    "",
    response_model=ProfileResponse,
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
    profile: ProfileOutSchema = await GetUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(user_id=current_user_id)

    return ProfileResponse(**profile.model_dump())


@profile_router.post(
    "",
    response_model=ProfileResponse,
)
async def create_profile(
    registration_data: ProfileRequestCreate,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Registrate users's Profile.

    Returns:
        The user's **Profile**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access is invalid
    """
    interests: Optional[list[Interest]] = await InterestReadOnlyRepository(
        db_session=db_session
    ).list(entry_ids=registration_data.interests)

    profile_data: ProfileInCreateSchema = ProfileInCreateSchema(
        **registration_data.model_dump(),
        owner_id=current_user_id,
    )

    profile: ProfileOutSchema = await GetOrCreateProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(
        profile_data=profile_data,
        interests=interests,
    )
    return ProfileResponse(**profile.model_dump())


@profile_router.patch(
    "",
    response_model=ProfileResponse,
)
async def update_profile(
    profile_data_to_update: ProfileRequestUpdate,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Registrate users's Profile.

    Returns:
        The user's **Profile**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access is invalid
    """

    interests: Optional[list[Interest]] = await InterestReadOnlyRepository(
        db_session=db_session
    ).list(entry_ids=profile_data_to_update.interests)

    profile_data: ProfileInUpdateSchema = ProfileInUpdateSchema(
        **profile_data_to_update.model_dump(),
        owner_id=current_user_id,
    )

    profile: ProfileOutSchema = await UpdateUserProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(
        profile_data=profile_data,
        interests=interests,
    )
    return ProfileResponse(**profile.model_dump())


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
