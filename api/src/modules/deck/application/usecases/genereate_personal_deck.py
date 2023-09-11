from uuid import UUID

from src.config.settings import settings

from src.core.usecases import IUseCase
from src.modules.deck.application.dtos.deck import DeckBatchOutDTO
from src.modules.deck.application.repositories import (
    IDeckCacheRepository,
    IDeckRepository,
)
from src.modules.deck.application.dtos import DeckProfileOutDTO
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound


class GenereatePersonalDeckUsecase(IUseCase):
    def __init__(
        self,
        *,
        deck_repository: IDeckRepository,
        profile_repository: IProfileRepository,
        deck_cache_repository: IDeckCacheRepository,
    ):
        self._deck_repo: IDeckRepository = deck_repository
        self._profile_repo: IProfileRepository = profile_repository
        self._deck_cache_repo: IDeckCacheRepository = deck_cache_repository

    async def execute(self, *, user_id: UUID) -> DeckBatchOutDTO:
        async with self._deck_repo, self._profile_repo, self._deck_cache_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            if not existent_profile:
                raise ProfileNotFound

            time_since_deck_creation: int | None = (
                await self._deck_cache_repo.get_time_since_creation_s(
                    profile_id=existent_profile.id
                )
            )
            profiles_to_fetch: list[UUID]
            if (
                time_since_deck_creation
                and time_since_deck_creation < settings.DECK_TTL_S
            ):
                profiles_to_fetch = await self._deck_cache_repo.get_batch(
                    profile_id=existent_profile.id,
                    batch_size=settings.DECK_BATCH_SIZE,
                )
            else:
                profiles_to_fetch = await self._deck_repo.generate(
                    profile_id=existent_profile.id
                )

            batch = await self._profile_repo.fetch(
                entities_ids=profiles_to_fetch[: settings.DECK_BATCH_SIZE]
            )

            await self._deck_cache_repo.save(
                profile_id=existent_profile.id,
                profiles=profiles_to_fetch[settings.DECK_BATCH_SIZE :],
            )

            batch_wit_distance = [
                DeckProfileOutDTO(
                    **profile.model_dump(),
                    coords_1=profile.location,
                    coords_2=existent_profile.location,
                )
                for profile in batch
            ]

            return DeckBatchOutDTO(batch=batch_wit_distance)
