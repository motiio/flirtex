from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.deck.application.repositories import ISkipRepository
from src.modules.deck.domain.entities import Skip
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound


class SkipUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
        skip_repository: ISkipRepository,
    ):
        self._skip_repo: ISkipRepository = skip_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(
        self,
        *,
        user_id: UUID,
        target_profile: UUID,
    ) -> None:
        async with self._skip_repo, self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            if not existent_profile:
                raise ProfileNotFound

            my_skip = await self._skip_repo.get_skip_by_profiles(
                target_profile=target_profile, source_profile=existent_profile.id
            )
            if my_skip:
                return None

            skip_entitie = Skip.create(
                source_profile=existent_profile.id, target_profile=target_profile
            )
            _ = await self._skip_repo.create(in_entity=skip_entitie)
