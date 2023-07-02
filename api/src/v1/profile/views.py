from collections.abc import Iterable
from fastapi import APIRouter

from src.v1.auth.dependencies.current_user import CurrentUser
from src.v1.config.database import DbSession
from src.v1.profile.dtos import ProfileRequestCreate, ProfileResponse
from src.v1.profile.models import Interest
from src.v1.profile.repositories.interest import InterestReadOnlyRepository
from src.v1.profile.repositories.profile import ProfileRepository
from src.v1.profile.schemas.interest import InterestOutSchema
from src.v1.profile.schemas.profile import ProfileInCreateSchema, ProfileOutSchema
from src.v1.profile.usecases.interest import ListInterests
from src.v1.profile.usecases.profile import GetOrCreateProfile

profile_router = APIRouter()


@profile_router.get(
    "/profile",
    # response_model=ProfileResponse,
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
    return current_user_id


@profile_router.post(
    "/profile",
    # response_model=ProfileResponse,
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
    interest: list[Interest] = await InterestReadOnlyRepository(
        db_session=db_session
    ).list(entry_ids=registration_data.interests)
    profile_data = ProfileInCreateSchema(
        **registration_data.model_dump(),
        owner_id=current_user_id,
    )
    profile: ProfileOutSchema = await GetOrCreateProfile(
        repository=ProfileRepository(db_session=db_session)
    ).execute(
        profile_data=profile_data,
        interests=interest,
    )
    return ProfileResponse(**profile.model_dump())
