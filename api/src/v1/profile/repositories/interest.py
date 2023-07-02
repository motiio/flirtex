from typing import Type

from src.v1.config.repositories import BaseRepository
from src.v1.profile.models import Interest
from src.v1.profile.schemas.interest import InterestInReadSchema


class InterestReadOnlyRepository(BaseRepository[InterestInReadSchema, Interest]):
    @property
    def _table(self) -> Type[Interest]:
        return Interest
