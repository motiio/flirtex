from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.entities import BaseEntity


@dataclass
class Interest(BaseEntity):
    id: UUID
    name: str
    icon: str

    def __init__(self, *, id: UUID, name: str, icon: str):
        self.id = id
        self.name = name
        self.icon = icon

    @classmethod
    def create(cls, *, id: UUID | None = None, name: str, icon: str, **kwargs) -> "Interest":
        if id is None:
            id = uuid4()

        interest = Interest(id=id, name=name, icon=icon)
        return interest
