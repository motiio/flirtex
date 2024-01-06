from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.deck.application.repositories import ILikeRepository, IMatchRepository
from src.modules.deck.domain.entities import Like, Match
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound, TargetProfileNotFound


class LikeUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
        like_repository: ILikeRepository,
        match_repository: IMatchRepository,
    ):
        self._like_repo: ILikeRepository = like_repository
        self._match_repo: IMatchRepository = match_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(  # type: ignore
        self,
        *,
        user_id: UUID,
        target_profile_id: UUID,
    ) -> None:
        async with self._like_repo, self._profile_repo, self._match_repo:
            source_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            target_profile = await self._profile_repo.get(entity_id=target_profile_id)

            if not source_profile:
                raise ProfileNotFound
            if not target_profile:
                raise TargetProfileNotFound

            my_like, his_like = await self._like_repo.get_likes_by_profiles(
                target_profile=target_profile.id, source_profile=source_profile.id
            )
            # если лайк этому профилю уже был поставлен = выход
            if my_like:
                return None

            # создаем сущность Like и добавляем в DB
            like_entitie = Like.create(
                source_profile=source_profile.id, target_profile=target_profile.id
            )
            my_like = await self._like_repo.create(in_entity=like_entitie)

            # Если лайк тебе не был поставлен, то выход
            if not his_like:
                return None

            # если также был найден лайк, который поставлен тебе, то это Match
            match_entitie = Match.create(
                profile_1=my_like.source_profile, profile_2=his_like.source_profile
            )
            _ = await self._match_repo.create(in_entity=match_entitie)
