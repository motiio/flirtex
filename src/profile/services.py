from sqlalchemy import insert, select

from src.database.core import DbSession
from src.profile.models import Profile

from .schemas import ProfileReadSchema


async def get_active_profile_by_user_id(db_session: DbSession, user_id: int) -> ProfileReadSchema:
    """Returns a user's profile"""
    q = select(Profile).where(Profile.owner == user_id, Profile.is_active == True)  # noqa
    return (await db_session.execute(q)).scalars().first()


async def create_profile(db_session: DbSession, profile_data: dict) -> ProfileReadSchema:
    print(profile_data)
    """Creates a new profile."""
    q = insert(Profile).values(**profile_data, is_active=True).returning(Profile)
    result = (await db_session.execute(q)).scalars().first()
    await db_session.commit()
    return ProfileReadSchema.from_orm(result)
