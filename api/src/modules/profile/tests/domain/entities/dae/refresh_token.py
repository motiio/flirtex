import uuid
from datetime import datetime, timedelta

import pytest

from src.modules.auth.application.utils.jwt import check_token_signature
from src.modules.auth.tests.infrastructure.factories.refresh_token_factory import (
    RefreshTokenFactory,
)

DAYS_7__SEC = 604800


@pytest.fixture()
def refresh_token_expiration() -> datetime:
    return datetime.now() + timedelta(days=30)


def test_refresh_token_expiration(refresh_token_expiration: datetime):
    refresh_token = RefreshTokenFactory()
    token, data = check_token_signature(token=str(refresh_token.value))

    assert token == refresh_token.value
    assert str(uuid.UUID(data["sub"])) == str(refresh_token.id)
    # Вызываем функцию generate_token с expiration_seconds = 30 дней (2592000 секунд)
    expiration_time = datetime.utcfromtimestamp(data["exp"])
    # Получаем текущую дату и время
    current_time = datetime.utcnow()
    # Проверяем, что дата истечения токена больше текущей даты и времени на 30 дней
    assert expiration_time.replace(minute=0, second=0, microsecond=0) == (
        current_time + timedelta(seconds=DAYS_7__SEC)
    ).replace(minute=0, second=0, microsecond=0)
