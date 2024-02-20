from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.deck.application.dtos import FilterInUpdateDTO, FilterOutDTO
from src.modules.deck.application.repositories.deck_cache import IDeckCacheRepository
from src.modules.deck.application.repositories.filter import IFilterRepository
from src.modules.deck.domain.exceptions import FilterNotFound
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound


class UpdateFilterUsecase(IUseCase):
    def __init__(
        self,
        *,
        filter_repository: IFilterRepository,
        profile_repository: IProfileRepository,
        deck_cache_repository: IDeckCacheRepository,
    ):
        self._filter_repo: IFilterRepository = filter_repository
        self._profile_repo: IProfileRepository = profile_repository
        self._deck_cache_repo: IDeckCacheRepository = deck_cache_repository

    async def execute(
        self,
        *,
        in_entity: FilterInUpdateDTO,
        user_id: UUID,
    ) -> FilterOutDTO:
        async with self._profile_repo, self._filter_repo, self._deck_cache_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            if not existent_profile:
                raise ProfileNotFound

            existent_filter = await self._filter_repo.get_by_profile(
                profile_id=existent_profile.id
            )
            if not existent_filter:
                raise FilterNotFound

            new_filter = existent_filter.update(**in_entity.model_dump())
            updated_filter = await self._filter_repo.update(in_entity=new_filter)
            await self._deck_cache_repo.delete(profile_id=existent_profile.id)

            return FilterOutDTO(**updated_filter.model_dump())
