from src.config.database import DbSession
from src.modules.auth.application.usecases.update_token import UpdateTokenUsecase
from src.modules.auth.infrastructure import (
    RefreshTokenRepository,
    UserRepository,
)


def update_token_service_factory(db_session: DbSession):
    user_repository = UserRepository(db_session=db_session)
    refresh_token_repository = RefreshTokenRepository(db_session=db_session)

    return UpdateTokenUsecase(
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )
