from fastapi import APIRouter

from src.auth.services import CurrentUser
from src.database.core import DbSession

from .schemas import CityReadSchema, InterestReadSchema
from .services import get_all_cities, get_all_interests

common_router = APIRouter()


@common_router.get("/cities", response_model=list[CityReadSchema])
async def get_cities(
        *,
        user: CurrentUser,
        db_session: DbSession,
) -> list[CityReadSchema]:
    print(123)
    return await get_all_cities(db_session=db_session)


@common_router.get("/interests", response_model=list[InterestReadSchema])
async def get_interests(
        *,
        user: CurrentUser,
        db_session: DbSession,
) -> list[InterestReadSchema]:
    return await get_all_interests(db_session=db_session)
