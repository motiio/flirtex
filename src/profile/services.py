from sqlalchemy import insert, select

from src.profile.models import City, Profile

from .schemas import ProfileRead


async def get_active_profile_by_user_id(*, db_session, user_id: int) -> ProfileRead:
    """Returns a user's profile"""
    q = select(Profile).where(Profile.owner == user_id, Profile.is_active is True)
    return (await db_session.execute(q)).fetchone()


async def create_profile(*, db_session, profile_data: ProfileRead) -> ProfileRead:
    q = (
        insert(Profile)
        .values(
            owner=int(profile_data.id),
            city=select(City.id).where(City.name == profile_data.city),
            **profile_data.dict(exclude={"id", "city"}),
        )
        .returning(Profile)
    )
    print(q)
    return (await db_session.execute(q)).one()
