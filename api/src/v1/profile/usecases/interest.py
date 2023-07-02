from uuid import UUID

from pydantic import TypeAdapter

from src.v1.config.usecases import BaseUseCase
from src.v1.profile.repositories.interest import InterestReadOnlyRepository
from src.v1.profile.schemas.interest import (
    InterestInReadSchema,
    InterestOutSchema,
)


class ListInterests(
    BaseUseCase[
        InterestReadOnlyRepository,
        InterestInReadSchema,
        InterestOutSchema,
    ]
):
    async def execute(self, *, interests_uuids: list[UUID]):
        async with self.repository as repo:
            interests = await repo.list(entry_ids=interests_uuids)
        return TypeAdapter(list[InterestOutSchema]).validate_python(interests)
