from uuid import UUID

from src.config.settings import settings
from src.core.repositories.implementations.redis import BaseRedisRepository
from src.modules.deck.application.repositories.deck_cache import IDeckCacheRepository
from src.modules.deck.domain.exceptions import DeckNoLongerExists


class DeckCacheRepository(BaseRedisRepository, IDeckCacheRepository):
    async def save(self, *, profile_id: UUID, profiles: list[UUID]) -> None:
        if not profiles:
            return
        await self._session.sadd(str(profile_id), *[str(profile_id) for profile_id in profiles])  # type: ignore
        await self._session.expire(str(profile_id), settings.DECK_TTL_S)

    async def get_batch(self, *, profile_id: UUID, batch_size=5) -> list[UUID]:
        is_deck_exists = await self._session.exists(str(profile_id))
        if not is_deck_exists:
            raise DeckNoLongerExists

        batch = await self._session.spop(str(profile_id), batch_size)  # type: ignore
        return batch

    async def delete(self, *, profile_id):
        await self._session.delete(str(profile_id))
