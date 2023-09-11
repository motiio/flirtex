from src.config.database import DbSession
from src.config.redis import DeckRedisSession
from src.modules.deck.application.usecases.genereate_personal_deck import (
    GenereatePersonalDeckUsecase,
)
from src.modules.deck.infrastructure.repositories.deck import DeckRepository
from src.modules.deck.infrastructure.repositories.deck_cache import DeckCacheRepository
from src.modules.profile.infrastructure.repositories.profile import ProfileRepository


def personal_deck_service_factory(
    db_session: DbSession,
    deck_redis_session: DeckRedisSession,
):
    deck_repository = DeckRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)
    deck_cache_repository = DeckCacheRepository(session=deck_redis_session)

    return GenereatePersonalDeckUsecase(
        deck_repository=deck_repository,
        profile_repository=profile_repository,
        deck_cache_repository=deck_cache_repository,
    )
