from uuid import UUID
from src.v1.config.database import DbSession
from src.v1.deck.repositories.db import LikeRepository, MatchRepository
from src.v1.deck.schemas import MatchInCreateSchema
from src.v1.deck.usecases import CheckMatch, CreateMatch


async def check_match(
    *, db_session: DbSession, source_profile: UUID, target_profile: UUID
):
    is_match = CheckMatch(repository=LikeRepository(db_session=db_session)).execute(
        source_profile=source_profile, target_profile=target_profile
    )
    if is_match:
        match_data = MatchInCreateSchema(
            profile_1=source_profile, profile_2=target_profile
        )
        await CreateMatch(repository=MatchRepository(db_session=db_session)).execute(
            in_schema=match_data
        )
        # TODO Notify service
        # await send notify
