from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_302_FOUND,
    HTTP_303_SEE_OTHER,
    HTTP_404_NOT_FOUND,
)

from src.auth.services import CurrentUser
from src.common.services import get_city_by_name
from src.database.core import DbSession

from .schemas import ProfileCreateSchema, ProfileReadSchema
from .services import create_profile, get_active_profile_by_user_id

profile_router = APIRouter()


@profile_router.post("", status_code=HTTP_201_CREATED, response_model=ProfileReadSchema)
async def register_profile(
    profile_data: ProfileCreateSchema,
    user: CurrentUser,
    db_session: DbSession,
):
    """
    Register a new profile for the current user.

    Args:
        profile_data: The profile data to register.
        user: The current user.
        db_session: The database session.

    Returns:
        The newly created profile.

    Raises:
        HTTPException: If the user already has a profile.
        HTTPException: If the city does not exist.
    """
    user_profile = await get_active_profile_by_user_id(db_session=db_session, user_id=user)
    if user_profile:
        raise HTTPException(
            status_code=HTTP_302_FOUND,
            detail=[
                {
                    "meta": {
                        "redirect": True,
                        "location": "/profile",
                    },
                    "msg": "User profile was found",
                }
            ],
        )
    city = await get_city_by_name(db_session=db_session, city_name=profile_data.city)
    print(city)
    print(city.id)
    if not city:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=[
                {
                    "msg": "City not found",
                }
            ],
        )
    register_data = ProfileCreateSchema(**profile_data.dict(exclude={"city"}) | {"city": city.id})
    return await create_profile(db_session=db_session, profile_data=register_data)


@profile_router.get("", response_model=ProfileReadSchema)
async def get_my_profile(
    *,
    user: CurrentUser,
    db_session: DbSession,
):
    """Returns the current user's profile."""
    print(user)
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
