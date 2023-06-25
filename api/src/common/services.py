from sqlalchemy import select

from src.database.core import DbSession
from src.profile.models import Interest


async def get_all_interests(
    *,
    db_session: DbSession,
) -> list[Interest]:
    """Returns all profile interests"""
    q = select(Interest)
    result = (await db_session.execute(q)).scalars().all()
    return list(result)
