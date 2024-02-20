from src.config.database import DbSession
from src.config.s3 import S3Session
from src.modules.profile.application.usecases import DeleteProfileUsecase
from src.modules.profile.infrastructure.repositories import (
    ProfileRepository,
)
from src.modules.profile.infrastructure.repositories.photo import (
    ProfilePhotoS3Repository,
)


def delete_profile_service_factory(db_session: DbSession, s3_session: S3Session):
    profile_repository = ProfileRepository(db_session=db_session)
    photo_s3_repo = ProfilePhotoS3Repository(s3_session=s3_session)

    return DeleteProfileUsecase(
        profile_repository=profile_repository, photo_s3_repo=photo_s3_repo
    )
