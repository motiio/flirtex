from fastapi import APIRouter

from src.auth.services import CurrentUser
from src.database.core import DbSession

from src.common.schemas import InterestOutResponse
from .services import get_all_interests

common_router = APIRouter()


@common_router.get(
    "/interests",
    response_model=list[InterestOutResponse],
)
async def get_interests(
    *,
    user: CurrentUser,
    db_session: DbSession,
) -> list[InterestOutResponse]:
    result = await get_all_interests(db_session=db_session)
    return list(result)
