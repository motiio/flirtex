from typing import Type

from src.v1.interest.models import Interest
from src.v1.base.repositories.db import BaseReadOnlyRepository


class InterestReadOnlyRepository(BaseReadOnlyRepository[Interest]):
    @property
    def _table(self) -> Type[Interest]:
        return Interest
