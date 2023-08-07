from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import ProfileNotFound


class DeleteProfileUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
    ):
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, owner_id: UUID) -> None:
        async with self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=owner_id)
            if not existent_profile:
                raise ProfileNotFound

            await self._profile_repo.delete(entity_id=existent_profile.id)
