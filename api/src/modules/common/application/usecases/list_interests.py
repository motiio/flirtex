from uuid import UUID

from src.core.usecases import IUseCase
from src.modules.common.application.dtos import InterestsOutDTO
from src.modules.profile.application.repositories.interest import IInterestRepository


class ListInterestUsecase(
    IUseCase[
        None,
        InterestsOutDTO,
    ],
):
    def __init__(
        self,
        *,
        interest_repository: IInterestRepository,
    ):
        self._interest_repo: IInterestRepository = interest_repository

    async def execute(self) -> InterestsOutDTO:
        async with self._interest_repo:
            all_interests = await self._interest_repo.list()

            return InterestsOutDTO(interests=all_interests)
