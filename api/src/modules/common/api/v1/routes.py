from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.modules.auth.application.dependencies import CurrentUser
from src.modules.common.application.dtos import InterestsOutDTO
from src.modules.common.dependencies import ListInterestsService

common_router = APIRouter(prefix="/common")


@common_router.get(
    "/interests",
    response_model=InterestsOutDTO,
    status_code=HTTP_200_OK,
)
async def get_all_interests(
    _: CurrentUser,
    list_interests_service: ListInterestsService,
):
    """
    All available interests.

    Returns:
        The list of **interests**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access token is invalid
    """
    all_interests = await list_interests_service.execute()

    return all_interests
