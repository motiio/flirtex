import factory

from src.modules.auth.api.v1.schemas.login import TelegramLoginRequestSchema
from src.modules.auth.application.dtos.telegram_login import TelegramLoginInDTO
from src.modules.auth.application.usecases.telegram_login import TelegramLoginUsecase
from src.modules.auth.tests.infrastructure.repositories import (
    RefreshTokenRepository,
    UserRepository,
)


def telegram_login_request_factory(
    request_data: dict,
) -> TelegramLoginRequestSchema:
    return TelegramLoginRequestSchema(**request_data)


def telegram_login_service_factory(db_session: dict):
    user_repository = UserRepository(db_session=db_session)
    refresh_token_repository = RefreshTokenRepository(db_session=db_session)

    return TelegramLoginUsecase(
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


class TelegramLoginInDTOFactory(factory.Factory):
    class Meta:
        model = TelegramLoginInDTO

    user_agent: str = "ua1"
    tg_login_data: dict = {
        "user": {
            "id": 99999999,
            "username": "user_1",
            "first_name": "FirstName1",
            "last_name": "LastName1",
            "is_premium": False,
            "language_code": "ru",
        }
    }
