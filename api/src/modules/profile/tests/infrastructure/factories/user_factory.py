from uuid import uuid4

import factory

from src.modules.auth.domain.entities.de.user import User
from src.modules.auth.infrastructure.models import UserORM


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = uuid4()
    tg_id = 9876
    tg_username = "user_1"
    tg_first_name = "FirstName1"
    tg_last_name = "LastName1"
    tg_is_premium = False
    tg_language_code = "RU"


class UserORMFactory(factory.Factory):
    class Meta:
        model = UserORM

    id = uuid4()
    tg_id = 9876
    tg_username = "user_1"
    tg_first_name = "FirstName1"
    tg_last_name = "LastName1"
    tg_is_premium = False
    tg_language_code = "RU"
