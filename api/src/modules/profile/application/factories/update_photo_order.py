from src.config.database import DbSession
from src.modules.profile.application.usecases.update_photo_order import (
    UpdatePhotoOrderUsecase,
)
from src.modules.profile.infrastructure.repositories import (
    ProfilePhotoRepository,
    ProfileRepository,
)


def update_photo_order_service_factory(db_session: DbSession):
    photo_repository = ProfilePhotoRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)
    return UpdatePhotoOrderUsecase(
        profile_repository=profile_repository,
        photo_repository=photo_repository,
    )
