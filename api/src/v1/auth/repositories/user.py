from typing import Type

from sqlalchemy import select

from src.v1.auth.models import User
from src.v1.auth.schemas.user import UserInCreateSchema, UserInUpdateSchema
from src.v1.repositories import BaseRepository


class UserRepository(BaseRepository[UserInCreateSchema, UserInUpdateSchema, User]):
    @property
    def _table(self) -> Type[User]:
        return User

    async def get_by_tg_id(self, *, tg_id: int) -> User | None:
        q = select(User).where(User.tg_id == tg_id)
        entry = (await self._db_session.execute(q)).scalars().first()
        return entry
