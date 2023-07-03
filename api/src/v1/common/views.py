from fastapi import APIRouter

from src.v1.auth.dependencies.current_user import CurrentUser
from src.v1.common.dtos import InterestsResponse
from src.v1.config.database import DbSession
from src.v1.profile.dtos import InterestsReadResponse
from src.v1.profile.repositories.interest import InterestReadOnlyRepository
from src.v1.profile.schemas.interest import InterestsOutSchema
from src.v1.profile.usecases.interest import ListInterests

common_router = APIRouter(prefix="/common")


@common_router.get(
    "/interests",
    response_model=InterestsReadResponse,
)
async def get_all_interests(
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    All available interests.

    Returns:
        The list of **interests**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access token is invalid
    """
    all_interests: InterestsOutSchema = await ListInterests(
        repository=InterestReadOnlyRepository(db_session=db_session)
    ).execute()

    return InterestsResponse(**all_interests.model_dump())
