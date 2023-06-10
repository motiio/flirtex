from pydantic import parse_obj_as
from sqlalchemy import select

from api.src.database.core import DbSession
from api.src.profile.models import Interest

from .models import City
from .schemas import CityReadSchema, InterestReadSchema


async def get_city_by_name(*, db_session: DbSession, city_name: str) -> CityReadSchema:
    """Returns a city by its name"""
    q = select(City).where(City.name == city_name)
    result = (await db_session.execute(q)).scalars().first()
    return CityReadSchema.from_orm(result)


async def get_city(*, db_session: DbSession, city_id: int) -> CityReadSchema:
    """Returns a city by its id"""
    q = select(City).where(City.id == city_id)
    result = (await db_session.execute(q)).scalars().first()
    return CityReadSchema.from_orm(result)


async def get_all_cities(*, db_session: DbSession) -> list[CityReadSchema]:
    """Returns all cities"""
    q = select(City).order_by(City.name)
    result = (await db_session.execute(q)).scalars().all()
    return parse_obj_as(list[CityReadSchema], result)


async def get_cities_by_region(*, db_session: DbSession, region_id: int) -> list[CityReadSchema]:
    """Returns all regions cities"""
    ...


async def get_all_interests(*, db_session: DbSession) -> list[InterestReadSchema]:
    """Returns all regions cities"""
    q = select(Interest)
    result = (await db_session.execute(q)).scalars().all()
    return parse_obj_as(list[InterestReadSchema], result)
