from src.config.database import DbSession
from src.modules.deck.application.usecases import GetLikeReactionsUsecase
from src.modules.deck.infrastructure.repositories import LikeRepository
from src.modules.profile.infrastructure.repositories.profile import ProfileRepository


def like_reactions_service_factory(db_session: DbSession):
    like_repository = LikeRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)

    return GetLikeReactionsUsecase(
        like_repository=like_repository,
        profile_repository=profile_repository,
    )
