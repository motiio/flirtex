from src.config.database import DbSession
from src.modules.deck.application.usecases import GetMatchesUsecase
from src.modules.deck.infrastructure.repositories import MatchRepository
from src.modules.profile.infrastructure.repositories.profile import ProfileRepository


def matches_service_factory(db_session: DbSession):
    match_repository = MatchRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)
    match_repository = MatchRepository(db_session=db_session)

    return GetMatchesUsecase(
        match_repository=match_repository,
        profile_repository=profile_repository,
    )
