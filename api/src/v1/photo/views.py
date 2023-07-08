from typing import Optional
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.v1.auth.dependencies.user import CurrentUser
from src.v1.interest.dtos import InterestsResponse
from src.v1.config.database import DbSession
from src.v1.photo.exceptions import PhotoNotFound
from src.v1.photo.repositories.db import PhotoRepository
from src.v1.profile.dtos import InterestsReadResponse
from src.v1.interest.repositories.db import InterestReadOnlyRepository
from src.v1.interest.schemas import InterestsOutSchema
from src.v1.interest.usecases import ListInterests

photo_router = APIRouter(prefix="/photo")


@photo_router.get(
    "/{short_url}",
)
async def get_all_interests(
    short_url: str,
    current_user_id: CurrentUser,
    db_session: DbSession,
):
    """
    Request photo by short url.

    Returns:
        The photo file.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's access token is invalid
    - HTTPExceptions: **HTTP_404_NOT_FOUND**. If photo by short url not found
    """
    redirect_url: Optional[str] = await PhotoRepository(
        db_session=db_session
    ).get_redirect_by_short_url(short_url=short_url)
    if not redirect_url:
        raise PhotoNotFound
    return RedirectResponse(url=redirect_url)
