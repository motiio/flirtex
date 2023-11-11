from typing import cast
from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.deck.application.dtos import LikeReactionProfileDTO, LikeReactionsDTO
from src.modules.deck.application.repositories import ILikeRepository
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import ProfileNotFound


class GetLikeReactionsUsecase(IUseCase):
    def __init__(
        self,
        *,
        like_repository: ILikeRepository,
        profile_repository: IProfileRepository,
    ):
        self._like_repo: ILikeRepository = like_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, user_id: UUID, limit: int, offset: int) -> LikeReactionsDTO:
        async with self._like_repo, self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            if not existent_profile:
                raise ProfileNotFound

            likes = await self._like_repo.get_likes_by_target(
                target_profile_id=existent_profile.id,
                limit=limit,
                offset=offset,
                order_by="-created_at",
            )

            like_reactions_profiles = await self._profile_repo.fetch(
                entities_ids=[like.source_profile for like in likes], ordering=True
            )

            return LikeReactionsDTO(
                profiles=cast(list[LikeReactionProfileDTO], like_reactions_profiles)
            )
