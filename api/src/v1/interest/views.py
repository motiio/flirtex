from fastapi import APIRouter

from src.v1.auth.dependencies.user import CurrentUser
from src.v1.config.database import DbSession
from src.v1.interest.dtos import InterestsResponse
from src.v1.interest.repositories.db import InterestReadOnlyRepository
from src.v1.interest.schemas import InterestsOutSchema
from src.v1.interest.usecases import ListInterests
from src.v1.profile.dtos import InterestsReadResponse

interest_router = APIRouter(prefix="/interests")


@interest_router.get(
    "",
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
