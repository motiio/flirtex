from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.entities import BaseEntity


@dataclass
class User(BaseEntity):
    id: UUID
    tg_id: int
    tg_username: str
    tg_first_name: str
    tg_last_name: str
    tg_is_premium: bool
    tg_language_code: str
    # _banned: bool

    def __init__(
        self,
        id: UUID,
        tg_id: int,
        tg_username: str,
        tg_first_name: str,
        tg_last_name: str,
        tg_is_premium: bool,
        tg_language_code: str,
        # banned: bool = False,
    ):
        self.id = id
        self.tg_id = tg_id
        self.tg_username = tg_username
        self.tg_first_name = tg_first_name
        self.tg_last_name = tg_last_name
        self.tg_is_premium = tg_is_premium
        self.tg_language_code = tg_language_code
        # self._banned = banned

    @classmethod
    def create(
        cls,
        *,
        id: UUID | None = None,
        tg_id: int,
        tg_username: str,
        tg_first_name: str,
        tg_last_name: str,
        tg_language_code: str,
        tg_is_premium: bool,
        # banned: bool = False,
        **kwargs,
    ) -> "User":
        if id is None:
            id = uuid4()

        user = User(
            id,
            tg_id,
            tg_username,
            tg_first_name,
            tg_last_name,
            tg_is_premium,
            tg_language_code,
            # banned,
        )
        return user

    def ban_user(self):
        self._is_banned = True

    def unban_user(self):
        self._is_banned = False

    def is_banned(self):
        return self._is_banned

    @property
    def str_id(self) -> str:
        return str(self.id)
