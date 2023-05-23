from pydantic import parse_obj_as
from sqlalchemy import select

from src.database.core import DbSession

from .models import City
from .schemas import CitySchema


async def get_city_by_name(*, db_session: DbSession, city_name: str) -> CitySchema:
    """Returns a city by its name"""
    q = select(City).where(City.name == city_name)
    result = (await db_session.execute(q)).scalars().one()
    return CitySchema.from_orm(result)


async def get_all_cities(*, db_session: DbSession) -> list[CitySchema]:
    q = select(City).order_by(City.name)
    result = (await db_session.execute(q)).scalars().all()
    return parse_obj_as(list[CitySchema], result)
