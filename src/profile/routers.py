from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_302_FOUND,
    HTTP_303_SEE_OTHER,
    HTTP_404_NOT_FOUND,
)

from src.auth.services import CurrentUser
from src.common.services import get_city
from src.database.core import DbSession

from .schemas import ProfileCreateRequest, ProfileReadSchema
from .services import create_profile, get_active_profile_by_user_id

profile_router = APIRouter()


@profile_router.post("", status_code=HTTP_201_CREATED, response_model=ProfileReadSchema)
async def register_profile(
    registration_data: ProfileCreateRequest,
    user: CurrentUser,
    db_session: DbSession,
):
    """
    Register a new profile for the current user.

    Args:
        registration_data: The profile data to register.
        user: The current user.
        db_session: The database session.

    Returns:
        The newly created profile.

    Raises:
        HTTPException: If the user already has a profile.
        HTTPException: If the city does not exist.
    """
    user_profile = await get_active_profile_by_user_id(db_session=db_session, user_id=int(user))
    if user_profile:
        raise HTTPException(
            status_code=HTTP_302_FOUND,
            detail=[
                {
                    "meta": {
                        "redirect": True,
                        "method": "GET",
                        "location": "/profile",
                    },
                    "msg": "User profile was found",
                }
            ],
        )
    city = await get_city(db_session=db_session, city_id=registration_data.city)
    if not city:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=[
                {
                    "msg": "City not found",
                }
            ],
        )
    profile_data = registration_data.dict() | {"owner": int(user)}
    return await create_profile(db_session=db_session, profile_data=profile_data)


@profile_router.get("", response_model=ProfileReadSchema)
async def get_my_profile(
    *,
    user: CurrentUser,
    db_session: DbSession,
):
    """Returns the current user's profile."""
    profile = await get_active_profile_by_user_id(db_session=db_session, user_id=int(user))
    if not profile:
        raise HTTPException(
            status_code=HTTP_303_SEE_OTHER,
            detail={
                "meta": {
                    "redirect": True,
                    "method": "POST",
                    "location": "/profile",
                },
                "msg": "User profile not found",
            },
        )
    return profile
