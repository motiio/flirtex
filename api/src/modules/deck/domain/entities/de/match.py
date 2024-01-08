from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.entities import BaseEntity


@dataclass
class Match(BaseEntity):
    id: UUID
    profile_1: UUID
    profile_2: UUID

    def __init__(self, id: UUID, profile_1: UUID, profile_2: UUID):
        self.id = id
        self.profile_1 = profile_1
        self.profile_2 = profile_2

    @classmethod
    def create(
        cls,
        *,
        id: UUID | None = None,
        profile_1: UUID,
        profile_2: UUID,
        **kwargs,
    ) -> "Match":
        if id is None:
            id = uuid4()

        match = Match(
            id,
            profile_1=profile_1,
            profile_2=profile_2,
        )
        return match

