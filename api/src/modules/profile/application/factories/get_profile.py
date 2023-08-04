from src.config.database import DbSession
from src.modules.profile.application.usecases import GetProfileUsecase
from src.modules.profile.infrastructure.repositories import (
    ProfileRepository,
)


def get_profile_service_factory(db_session: DbSession):
    profile_repository = ProfileRepository(db_session=db_session)

    return GetProfileUsecase(profile_repository=profile_repository)
