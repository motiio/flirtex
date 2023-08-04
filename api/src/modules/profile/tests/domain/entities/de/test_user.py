import uuid

from src.modules.auth.tests.infrastructure.factories.user_factory import (
    UserFactory,
)


def test_user_uuid():
    user = UserFactory()
    assert uuid.UUID(str(user.id)) == user.id
