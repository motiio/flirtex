from sqlalchemy.util.langhelpers import repr_tuple_names
from src.core.usecases import IUseCase
from src.modules.deck.application.dtos import (
    MatchOutDTO,
)
from src.modules.deck.application.repositories import ILikeRepository, IMatchRepository
from src.modules.deck.domain.entities import Like, Match
from src.modules.profile.application.repositories.profile import IProfileRepository
from src.modules.profile.domain.exceptions import ProfileNotFound
from uuid import UUID


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

    async def execute(
        self,
        *,
        user_id: UUID,
        target_profile: UUID,
    ) -> MatchOutDTO | None:
        async with self._like_repo, self._profile_repo, self._match_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            if not existent_profile:
                raise ProfileNotFound

            my_like, side_like = await self._like_repo.get_likes_by_profiles(
                target_profile=target_profile, source_profile=existent_profile.id
            )
            # если лайк этому профилю уже был поставлен
            if my_like:
                return None

            like_entitie = Like.create(
                source_profile=existent_profile.id, target_profile=target_profile
            )
            my_like = await self._like_repo.create(in_entity=like_entitie)
            if not side_like:
                return None

            match_entitie = Match.create(
                profile_1=my_like.source_profile, profile_2=side_like.source_profile
            )
            match = await self._match_repo.create(in_entity=match_entitie)
            return MatchOutDTO(**match.model_dump())