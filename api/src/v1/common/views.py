from pydantic import APIRouter
from src.v1.auth.dependencies.current_user import CurrentUser
from src.v1.config.database import DbSession
from src.v1.common.dtos import InterestsResponse

auth_router = APIRouter(prefix="/common")


@auth_router.get("/interests", response_model=InterestsResponse)
async def update_token_pair(
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    All available interests.

    Returns:
        The list of **interests**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access token is invalid
    """
    interests: Optional[list[Interest]] = await InterestReadOnlyRepository(
        db_session=db_session
    ).list(entry_ids=registration_data.interests)

    return InterestsResponse(interests=[])
