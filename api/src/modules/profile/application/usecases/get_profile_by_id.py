from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.profile.application.dtos import (
    ProfileWithDistanceOutDTO,
)
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import ProfileNotFound


class GetProfileByIdUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
    ):
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(
        self, wanted_profile_id: UUID, owner_id: UUID
    ) -> ProfileWithDistanceOutDTO:
        async with self._profile_repo:
            owner_profile = await self._profile_repo.get_by_owner(owner_id=owner_id)
            if not owner_profile:
                raise ProfileNotFound
            wanted_profile = await self._profile_repo.get(entity_id=wanted_profile_id)
            if not wanted_profile:
                raise ProfileNotFound

            return ProfileWithDistanceOutDTO(
                **wanted_profile.model_dump(),
                coords_1=owner_profile.location,
                coords_2=wanted_profile.location,
            )
