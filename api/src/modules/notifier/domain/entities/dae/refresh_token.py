from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.entities import BaseEntity


@dataclass
class RefreshTokenDAE(BaseEntity):
    id: UUID
    user: UUID
    user_agent: str
    value: str

    def __init__(self, id: UUID, user: UUID, user_agent: str, value: str):
        self.id = id
        self.user = user
        self.user_agent = user_agent
        self.value = value

    @classmethod
    def create(cls, *, id=None, user, user_agent, value: str, **kwargs):
        if id is None:
            id = uuid4()
        refresh_token = RefreshTokenDAE(id, user, user_agent, value)
        return refresh_token
