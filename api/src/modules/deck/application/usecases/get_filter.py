from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.deck.application.dtos import (
    FilterOutDTO,
)
from src.modules.deck.application.repositories.filter import IFilterRepository
from src.modules.deck.domain.exceptions import FilterNotFound
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound


class GetFilterUsecase(IUseCase):
    def __init__(
        self,
        *,
        filter_repository: IFilterRepository,
        profile_repository: IProfileRepository,
    ):
        self._filter_repo: IFilterRepository = filter_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, *, user_id: UUID) -> FilterOutDTO:
        async with self._filter_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            if not existent_profile:
                raise ProfileNotFound

            existent_filter = await self._filter_repo.get_by_profile(profile_id=existent_profile.id)
            if not existent_filter:
                raise FilterNotFound
            return FilterOutDTO(**existent_filter.model_dump())
