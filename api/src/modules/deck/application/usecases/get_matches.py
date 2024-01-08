from typing import cast
from uuid import UUID

from src.core.types import Pagination
from src.core.usecases import IUseCase
from src.modules.deck.application.dtos import MatchesOutDTO, MatchProfileOutDTO
from src.modules.deck.application.repositories import IMatchRepository
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import ProfileNotFound


class GetMatchesUsecase(IUseCase):
    def __init__(
        self,
        *,
        match_repository: IMatchRepository,
        profile_repository: IProfileRepository,
    ):
        self._match_repo: IMatchRepository = match_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(
        self, user_id: UUID, limit: int, offset: int
    ) -> tuple[MatchesOutDTO, Pagination]:
        async with self._match_repo, self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=user_id)
            if not existent_profile:
                raise ProfileNotFound

            match_profiles, pagination = await self._match_repo.get_match_profiles(
                profile_id=existent_profile.id,
                limit=limit,
                offset=offset,
                order_by='-"match".created_at',
            )
            return (
                MatchesOutDTO(profiles=cast(list[MatchProfileOutDTO], match_profiles)),
                pagination,
            )
