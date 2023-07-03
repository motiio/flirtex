from typing import Type

from src.v1.repositories import BaseReadOnlyRepository
from src.v1.profile.models import Interest
from src.v1.profile.schemas.interest import InterestInReadSchema


class InterestReadOnlyRepository(
    BaseReadOnlyRepository[InterestInReadSchema, Interest]
):
    @property
    def _table(self) -> Type[Interest]:
        return Interest
