from uuid import UUID

from geopy.distance import geodesic
from pydantic import computed_field

from src.core.dtos import BaseDTO
from src.modules.profile.application.dtos.interest import InterestOutDTO
from src.modules.profile.application.dtos.photo import PhotoOutDTO
from src.modules.profile.application.utils import enums as profile_enums
from src.modules.profile.domain.entities.types import Location


class DeckProfileOutDTO(BaseDTO):
    id: UUID
    name: str
    bio: str | None
    age: int
    gender: profile_enums.GenderEnum
    interests: list[InterestOutDTO] | None = None
    photos: list[PhotoOutDTO] | None = None
    coords_1: Location | None = None
    coords_2: Location | None = None

    @computed_field
    @property
    def distance(self) -> int | None:
        if self.coords_1 is None or self.coords_2 is None:
            return None
        return round(
            geodesic(
                (self.coords_1["latitude"], self.coords_1["longitude"]),
                (self.coords_2["latitude"], self.coords_1["longitude"]),
            ).kilometers
        )


class DeckBatchOutDTO(BaseDTO):
    batch: list[DeckProfileOutDTO]
