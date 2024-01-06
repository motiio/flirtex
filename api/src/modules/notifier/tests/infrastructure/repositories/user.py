from typing import Type

from src.core.repositories.implementations.in_memory import (
    BaseInMemorySqlAlchemnyRepository,
)
from src.modules.auth.application.repositories.user import IUserRepository
from src.modules.auth.domain.entities.de.user import User
from src.modules.auth.infrastructure.models import UserORM


class UserRepository(
    BaseInMemorySqlAlchemnyRepository[
        User,
        UserORM,
    ],
    IUserRepository,
):
    @property
    def _table(self) -> Type[UserORM]:
        return UserORM

    @property
    def _entity(self) -> Type[User]:
        return User

    async def get_by_tg_id(self, *, tg_id: int) -> User | None:
        result = [
            value
            for _, value in self._db_session.items()
            if isinstance(value, UserORM) and value.tg_id == tg_id
        ]
        if result:
            return self._entity.create(**result[0].dict())

        return None
