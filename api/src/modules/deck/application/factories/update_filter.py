from src.config.database import DbSession
from src.config.redis import DeckRedisSession
from src.modules.deck.application.usecases.update_filter import UpdateFilterUsecase
from src.modules.deck.infrastructure.repositories.deck_cache import DeckCacheRepository
from src.modules.deck.infrastructure.repositories.filter import FilterRepository
from src.modules.profile.infrastructure.repositories.profile import ProfileRepository


def update_filter_service_factory(
    db_session: DbSession,
    deck_redis_session: DeckRedisSession,
):
    filter_repository = FilterRepository(db_session=db_session)
    profile_repository = ProfileRepository(db_session=db_session)
    deck_cache_repository = DeckCacheRepository(session=deck_redis_session)

    return UpdateFilterUsecase(
        filter_repository=filter_repository,
        profile_repository=profile_repository,
        deck_cache_repository=deck_cache_repository,
    )
