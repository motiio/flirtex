from typing import Type

from src.v1.profile.models import Interest
from src.v1.profile.schemas.interest import InterestInReadSchema
from src.v1.repositories import BaseReadOnlyRepository


class InterestReadOnlyRepository(BaseReadOnlyRepository[InterestInReadSchema, Interest]):
    @property
    def _table(self) -> Type[Interest]:
        return Interest
