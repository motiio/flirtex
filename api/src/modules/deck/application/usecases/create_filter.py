from src.core.usecases import IUseCase
from src.modules.deck.application.dtos import (
    FilterInCreateDTO,
    FilterOutDTO,
)
from src.modules.deck.application.repositories.filter import IFilterRepository
from src.modules.deck.domain.entities import Filter
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound


class CreateFilterUsecase(IUseCase):
    def __init__(
        self,
        *,
        filter_repository: IFilterRepository,
        profile_repository: IProfileRepository,
    ):
        self._filter_repo: IFilterRepository = filter_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, *, in_dto: FilterInCreateDTO) -> FilterOutDTO:
        async with self._filter_repo:
            existent_profile = await self._profile_repo.get(entity_id=in_dto.profile_id)
            if not existent_profile:
                raise ProfileNotFound

            existent_filter = await self._filter_repo.get_by_profile(profile_id=existent_profile.id)
            if existent_filter:
                return FilterOutDTO(**existent_filter.model_dump())

            filter_entity = Filter.create(
                looking_gender=in_dto.looking_gender,
                age_from=in_dto.age_from,
                age_to=in_dto.age_to,
                profile_id=in_dto.profile_id,
            )
            created_filter = await self._filter_repo.create(in_entity=filter_entity)
            return FilterOutDTO(**created_filter.model_dump())
