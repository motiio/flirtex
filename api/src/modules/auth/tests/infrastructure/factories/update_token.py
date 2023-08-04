import factory

from src.config.settings import settings
from src.modules.auth.api.v1.schemas.login import TelegramLoginRequestSchema
from src.modules.auth.application.dtos.telegram_login import TelegramLoginInDTO
from src.modules.auth.application.usecases.telegram_login import TelegramLoginUsecase
from src.modules.auth.application.utils.jwt import generate_token
from src.modules.auth.tests.infrastructure.repositories import (
    RefreshTokenRepository,
    UserRepository,
)


def update_token_request_factory(
    request_data: dict,
) -> TelegramLoginRequestSchema:
    return TelegramLoginRequestSchema(**request_data)


def update_token_service_factory(db_session: dict):
    user_repository = UserRepository(db_session=db_session)
    refresh_token_repository = RefreshTokenRepository(db_session=db_session)

    return TelegramLoginUsecase(
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


class UpdateTokenInDTOFactory(factory.Factory):
    class Meta:
        model = TelegramLoginInDTO

    user_agent: str = "ua1"
    user: str = "bff23be7-ab7f-48f1-a814-7b257736632c"

    @factory.lazy_attribute
    def refresh_token(self) -> str:
        value = generate_token(
            sub=str(self.user),
            secret=settings.JWT_SECRET,
            expiration_seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
        )
        return value
