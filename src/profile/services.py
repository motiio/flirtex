from sqlalchemy import insert, select

from src.database.core import DbSession
from src.profile.models import Profile

from .schemas import ProfileReadSchema, ProfileSchema


async def get_active_profile_by_user_id(db_session: DbSession, user_id: int) -> ProfileReadSchema:
    """Returns a user's profile"""
    q = select(Profile).where(Profile.owner == user_id, Profile.is_active is True)
    return (await db_session.execute(q)).fetchone()


async def create_profile(db_session: DbSession, profile_data: ProfileSchema) -> ProfileReadSchema:
    """Creates a new profile."""
    q = (
        insert(Profile)
        .values(**profile_data.dict())
        .returning(Profile.id, Profile.name, Profile.birthdate, Profile.city)
    )
    result = (await db_session.execute(q)).fetchone()
    return ProfileReadSchema(**result.first())
