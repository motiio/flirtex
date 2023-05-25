from pydantic import parse_obj_as
from sqlalchemy import select

from src.database.core import DbSession

from .models import City
from .schemas import CitySchema


async def get_city_by_name(*, db_session: DbSession, city_name: str) -> CitySchema:
    """Returns a city by its name"""
    q = select(City).where(City.name == city_name)
    result = (await db_session.execute(q)).scalars().first()
    return CitySchema.from_orm(result)


async def get_city(*, db_session: DbSession, city_id: int) -> CitySchema:
    """Returns a city by its id"""
    q = select(City).where(City.id == city_id)
    result = (await db_session.execute(q)).scalars().first()
    return CitySchema.from_orm(result)


async def get_all_cities(*, db_session: DbSession) -> list[CitySchema]:
    """Returns all cities"""
    q = select(City).order_by(City.name)
    result = (await db_session.execute(q)).scalars().all()
    return parse_obj_as(list[CitySchema], result)


async def get_cities_by_region(*, db_session: DbSession, region_id: int) -> list[CitySchema]:
    """Returns all regions cities"""
    ...
