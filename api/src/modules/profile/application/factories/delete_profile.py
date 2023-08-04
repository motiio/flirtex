from src.config.database import DbSession
from src.modules.profile.application.usecases import DeleteProfileUsecase
from src.modules.profile.infrastructure.repositories import (
    ProfileRepository,
)


def delete_profile_service_factory(db_session: DbSession):
    profile_repository = ProfileRepository(db_session=db_session)

    return DeleteProfileUsecase(profile_repository=profile_repository)
