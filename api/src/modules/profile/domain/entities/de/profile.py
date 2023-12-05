from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

import src.modules.profile.domain.entities.types as types
from src.core.entities import BaseEntity
from src.modules.profile.domain.entities.de.profile_photo import ProfilePhoto

from .interest import Interest


@dataclass
class Profile(BaseEntity):
    id: UUID
    name: str
    bio: str
    birthdate: date
    gender: int
    interests: list[Interest]
    photos: list[ProfilePhoto]
    owner_id: UUID
    location: types.Location | None

    # _banned: bool

    def __init__(
        self,
        *,
        id: UUID,
        name: str,
        bio: str,
        birthdate: date,
        gender: int,
        owner_id: UUID,
    ):
        self.id = id
        self.name = name
        self.bio = bio
        self.birthdate = birthdate
        self.gender = gender
        self.interests = []
        self.owner_id = owner_id
        self.photos = []
        self.location = None
        # self._banned = banned

    @classmethod
    def create(
        cls,
        *,
        id: UUID | None = None,
        name: str,
        bio: str | None = None,
        birthdate: date,
        gender: int,
        owner_id: UUID,
        **kwargs,
    ) -> "Profile":
        if id is None:
            id = uuid4()

        user = Profile(
            id=id,
            name=name,
            bio=bio,
            birthdate=birthdate,
            gender=gender,
            owner_id=owner_id,
        )
        return user

    def put_interests(self, interests: list[Interest]):
        self.interests = interests

    def add_photos(self, photos: list[ProfilePhoto]):
        self.photos = photos

    def put_location(self, *, location: types.Location | None):
        self.location = location

    @classmethod
    def _calculate_age(cls, *, birthdate: date) -> int:
        today = date.today()

        # A bool that represents if today's day/month precedes the birth day/month
        one_or_zero = (today.month, today.day) < (
            birthdate.month,
            birthdate.day,
        )

        # Calculate the difference in years from the date object's components
        year_difference = today.year - birthdate.year

        age = year_difference - one_or_zero

        return age

    @property
    def wkt_point(self) -> str | None:
        if self.location is None:
            return None
        return f"POINT({self.location['longitude']} {self.location['latitude']})"

    @property
    def age(self) -> int:
        return self._calculate_age(birthdate=self.birthdate)
