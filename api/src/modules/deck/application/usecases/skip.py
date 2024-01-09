from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.deck.application.repositories import ISkipRepository
from src.modules.deck.domain.entities import Skip
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound, TargetProfileNotFound


class SkipUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
        skip_repository: ISkipRepository,
    ):
        self._skip_repo: ISkipRepository = skip_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(  # type: ignore
        self,
        *,
        user_id: UUID,
        target_profile_id: UUID,
    ) -> None:
        async with self._skip_repo, self._profile_repo:
            source_profile = await self._profile_repo.get_by_owner(owner_id=user_id)

            target_profile = await self._profile_repo.get(entity_id=target_profile_id)

            if not source_profile:
                raise ProfileNotFound

            if not target_profile:
                raise TargetProfileNotFound

            my_skip = await self._skip_repo.get_skip_by_profiles(
                target_profile=target_profile.id, source_profile=source_profile.id
            )
            if my_skip:
                return None

            skip_entitie = Skip.create(
                source_profile=source_profile.id, target_profile=target_profile.id
            )
            _ = await self._skip_repo.create(in_entity=skip_entitie)
