from src.config.database import DbSession
from src.modules.deck.application.usecases import GetFilterUsecase
from src.modules.deck.infrastructure.repositories.filter import FilterRepository
from src.modules.profile.infrastructure.repositories.profile import ProfileRepository


def get_filter_service_factory(db_session: DbSession):
    filter_repository = FilterRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)

    return GetFilterUsecase(
        filter_repository=filter_repository,
        profile_repository=profile_repository,
    )
