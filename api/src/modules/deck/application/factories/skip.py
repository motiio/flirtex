from src.config.database import DbSession
from src.modules.deck.application.usecases import SkipUsecase
from src.modules.deck.infrastructure.repositories import SkipRepository, LikeRepository
from src.modules.profile.infrastructure.repositories.profile import ProfileRepository


def skip_service_factory(db_session: DbSession):
    skip_repository = SkipRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)
    like_repository = LikeRepository(db_session=db_session)

    return SkipUsecase(
        skip_repository=skip_repository,
        like_repository=like_repository,
        profile_repository=profile_repository,
    )
