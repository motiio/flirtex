from uuid import UUID

from src.core.repositories.implementations.redis import BaseRedisRepository
from src.modules.deck.application.repositories.deck_cache import IDeckCacheRepository
import time


class DeckCacheRepository(BaseRedisRepository, IDeckCacheRepository):
    async def save(self, *, profile_id: UUID, profiles: list[UUID]) -> None:
        if not profiles:
            return
        await self._session.sadd(str(profile_id), *[str(profile_id) for profile_id in profiles])  # type: ignore
        await self._session.set(str(profile_id) + "__created_at", time.time())

    async def get_batch(self, *, profile_id: UUID, batch_size=5) -> list[UUID]:
        batch = await self._session.spop(str(profile_id), batch_size)  # type: ignore
        return batch

    async def get_time_since_creation_s(self, *, profile_id: UUID) -> int | None:
        created_at = await self._session.get(name=str(profile_id) + "__created_at")
        if not created_at:
            return None

        since_creation = time.time() - float(created_at)
        return int(since_creation)

    async def remove_deck(self, *, profile_id):
        await self._session.delete(str(profile_id) + "__created_at", str(profile_id))
