from src.config.database import DbSession
from src.modules.profile.application.usecases import GetProfileByIdUsecase
from src.modules.profile.infrastructure.repositories import (
    ProfileRepository,
)


def get_profile_by_id_service_factory(db_session: DbSession):
    profile_repository = ProfileRepository(db_session=db_session)

    return GetProfileByIdUsecase(profile_repository=profile_repository)
