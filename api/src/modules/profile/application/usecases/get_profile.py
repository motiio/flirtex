from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.profile.application.dtos import (
    ProfileOutDTO,
    UpdateProfileInDTO,
)
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import ProfileNotFound


class GetProfileUsecase(
    IUseCase[
        UpdateProfileInDTO,
        ProfileOutDTO,
    ],
):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
    ):
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, owner_id: UUID) -> ProfileOutDTO:
        async with self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=owner_id)
            if not existent_profile:
                raise ProfileNotFound

            return ProfileOutDTO(**existent_profile.model_dump())
