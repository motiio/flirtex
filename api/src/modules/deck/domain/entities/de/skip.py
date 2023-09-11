from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.entities import BaseEntity


@dataclass
class Skip(BaseEntity):
    id: UUID
    source_profile: UUID
    target_profile: UUID
    # _banned: bool

    def __init__(self, id: UUID, source_profile: UUID, target_profile: UUID):
        self.id = id
        self.source_profile = source_profile
        self.target_profile = target_profile

    @classmethod
    def create(
        cls,
        *,
        id: UUID | None = None,
        source_profile: UUID,
        target_profile: UUID,
        **kwargs,
    ) -> "Skip":
        if id is None:
            id = uuid4()

        skip = Skip(
            id,
            source_profile=source_profile,
            target_profile=target_profile,
        )
        return skip
