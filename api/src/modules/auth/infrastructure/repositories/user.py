from typing import Type

from sqlalchemy import select

from core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from auth.application.repositories.user import IUserRepository
from auth.domain.entities import User
from auth.infrastructure.models import UserORM


class UserRepository(
    BaseSqlAlchemyRepository[
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
        q = select(self._table).where(self._table.tg_id == tg_id)
        result = (await self._db_session.execute(q)).scalars().first()

        if result:
            return self._entity.create(**result.dict())

        return None
