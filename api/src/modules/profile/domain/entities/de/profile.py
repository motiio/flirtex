from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from src.core.entities import BaseEntity
from src.modules.profile.domain.entities.dae.profile_photo import PhotoDAE

from .interest import Interest


@dataclass
class Profile(BaseEntity):
    id: UUID
    name: str
    bio: str
    birthdate: date
    gender: int
    looking_gender: int
    interests: list[Interest]
    photos: list[PhotoDAE]
    owner_id: UUID

    # _banned: bool

    def __init__(
        self,
        *,
        id: UUID,
        name: str,
        bio: str,
        birthdate: date,
        gender: int,
        looking_gender: int,
        # interests: list[Interest],
        owner_id: UUID,
    ):
        self.id = id
        self.name = name
        self.bio = bio
        self.birthdate = birthdate
        self.gender = gender
        self.looking_gender = looking_gender
        self.interests = []
        self.owner_id = owner_id
        # self._banned = banned

    @classmethod
    def create(
        cls,
        *,
        id: UUID | None = None,
        name: str,
        bio: str,
        birthdate: date,
        gender: int,
        looking_gender: int,
        # interests: list[Interest] | None = None,
        owner_id: UUID,
        **kwargs,
    ) -> "Profile":
        if id is None:
            id = uuid4()

        # if interests is None:
        # interests = []

        user = Profile(
            id=id,
            name=name,
            bio=bio,
            birthdate=birthdate,
            gender=gender,
            looking_gender=looking_gender,
            # interests=interests,
            owner_id=owner_id
            # banned,
        )
        return user

    def put_interests(self, interests: list[Interest]):
        self.interests = interests

    def add_photos(self, photos: list[PhotoDAE]):
        self.photos = photos
