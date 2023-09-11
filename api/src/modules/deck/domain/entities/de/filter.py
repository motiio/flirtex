from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.entities import BaseEntity


@dataclass
class Filter(BaseEntity):
    id: UUID
    looking_gender: int
    age_from: int
    age_to: int
    max_distance: int
    profile_id: UUID

    def __init__(
        self,
        *,
        id: UUID,
        looking_gender: int,
        age_from: int,
        age_to: int,
        max_distance: int,
        profile_id: UUID,
    ):
        self.id = id
        self.looking_gender = looking_gender
        self.age_from = age_from
        self.age_to = age_to
        self.max_distance = max_distance
        self.profile_id = profile_id

    @classmethod
    def create(
        cls,
        *,
        id: UUID | None = None,
        looking_gender: int,
        age_from: int,
        age_to: int,
        max_distance: int = 10,
        profile_id: UUID,
        **kwargs,
    ) -> "Filter":
        filter = Filter(
            id=id or uuid4(),
            looking_gender=looking_gender,
            age_from=age_from,
            age_to=age_to,
            max_distance=max_distance,
            profile_id=profile_id,
        )
        return filter

    def update(
        self,
        looking_gender: int | None = None,
        age_from: int | None = None,
        age_to: int | None = None,
        max_distance: int | None = None,
    ) -> "Filter":
        self.looking_gender = looking_gender or self.looking_gender
        self.age_from = age_from or self.age_from
        self.age_to = age_to or self.age_to
        self.max_distance = max_distance or self.max_distance

        return self
