from src.config.database import DbSession
from src.config.s3 import S3Session
from src.modules.profile.application.usecases import (
    DeleteProfilePhotoUsecase,
)
from src.modules.profile.infrastructure.repositories import (
    ProfilePhotoRepository,
    ProfilePhotoS3Repository,
    ProfileRepository,
)


def delete_profile_photo_service_factory(s3_session: S3Session, db_session: DbSession):
    profile_repository = ProfileRepository(db_session=db_session)
    photo_s3_repository = ProfilePhotoS3Repository(s3_session=s3_session)
    photo_repository = ProfilePhotoRepository(db_session=db_session)

    return DeleteProfilePhotoUsecase(
        profile_repository=profile_repository,
        photo_repository=photo_repository,
        photo_s3_repository=photo_s3_repository,
    )
