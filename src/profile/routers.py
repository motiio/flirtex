from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_302_FOUND, HTTP_303_SEE_OTHER

from src.auth.services import CurrentUser
from src.database.core import DbSession

from .schemas import ProfileRead
from .services import create_profile, get_active_profile_by_user_id

profile_router = APIRouter()


@profile_router.post("/register", status_code=HTTP_201_CREATED, response_model=ProfileRead)
async def register_profile(
    profile_data: ProfileRead,
    user: CurrentUser,
    db_session: DbSession,
):
    user_profile = await get_active_profile_by_user_id(db_session=db_session, user_id=user)
    if user_profile:
        raise HTTPException(
            status_code=HTTP_302_FOUND,
            detail=[
                {
                    "meta": {
                        "redirect": True,
                        "location": "/profile/me",
                    },
                    "msg": "User profile was found",
                }
            ],
        )
    return await create_profile(db_session=db_session, profile_data=profile_data)


@profile_router.get("/me", response_model=ProfileRead)
async def get_my_profile(
    *,
    user: CurrentUser,
    db_session: DbSession,
):
    profile = await get_active_profile_by_user_id(db_session=db_session, user_id=user)
    if not profile:
        raise HTTPException(
            status_code=HTTP_303_SEE_OTHER,
            detail=[
                {
                    "meta": {
                        "redirect": True,
                        "location": "/profile/register",
                    },
                    "msg": "User profile not found",
                }
            ],
        )
    else:
        return profile
