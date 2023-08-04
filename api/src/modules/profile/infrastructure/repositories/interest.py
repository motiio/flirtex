from typing import Type

from src.core.repositories.implementations.sqlalchemy import BaseSqlAlchemyRepository
from src.modules.profile.application.repositories import IInterestRepository
from src.modules.profile.domain.entities import Interest
from src.modules.profile.infrastructure.models import InterestORM


class InterestRepository(
    BaseSqlAlchemyRepository[
        Interest,
        InterestORM,
    ],
    IInterestRepository,
):
    @property
    def _table(self) -> Type[InterestORM]:
        return InterestORM

    @property
    def _entity(self) -> Type[Interest]:
        return Interest
