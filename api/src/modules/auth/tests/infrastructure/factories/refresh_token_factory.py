from uuid import uuid4

import factory

from src.config.settings import settings
from src.modules.auth.application.utils.jwt import generate_token
from src.modules.auth.domain.entities.dae.refresh_token import RefreshTokenDAE
from src.modules.auth.infrastructure.models import RefreshTokenORM


class RefreshTokenFactory(factory.Factory):
    class Meta:
        model = RefreshTokenDAE

    id = uuid4()
    user = uuid4()
    user_agent = "ua1"

    @factory.lazy_attribute
    def value(self) -> str:
        value = generate_token(
            sub=str(self.id),
            secret=settings.JWT_SECRET,
            expiration_seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
        )
        return value


class RefreshTokenORMFactory(factory.Factory):
    class Meta:
        model = RefreshTokenORM

    id = uuid4()
    user = uuid4()
    user_agent = "ua1"
