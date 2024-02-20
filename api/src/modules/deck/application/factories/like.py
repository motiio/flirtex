from src.config.database import DbSession
from src.modules.deck.application.usecases import LikeUsecase
from src.modules.deck.infrastructure.repositories import (
    LikeRepository,
    MatchRepository,
    SkipRepository,
)
from src.modules.profile.infrastructure.repositories.profile import ProfileRepository


def like_service_factory(db_session: DbSession):
    like_repository = LikeRepository(db_session=db_session)
    skip_repository = SkipRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)
    match_repository = MatchRepository(db_session=db_session)

    return LikeUsecase(
        match_repository=match_repository,
        like_repository=like_repository,
        skip_repository=skip_repository,
        profile_repository=profile_repository,
    )
