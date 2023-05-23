from fastapi import APIRouter

from src.auth.services import CurrentUser
from src.database.core import DbSession

from .schemas import CitySchema
from .services import get_all_cities

common_router = APIRouter()


@common_router.get("/cities", response_model=list[CitySchema])
async def get_cities(
    user: CurrentUser,
    db_session: DbSession,
) -> list[CitySchema]:
    return await get_all_cities(db_session=db_session)
