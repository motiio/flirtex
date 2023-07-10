from uuid import UUID

from pydantic import TypeAdapter

from src.v1.base.usecases import BaseUseCase
from src.v1.interest.repositories.db import InterestReadOnlyRepository
from src.v1.interest.schemas import (
    InterestInReadSchema,
    InterestOutSchema,
    InterestsOutSchema,
)


class FetchInterests(
    BaseUseCase[
        InterestReadOnlyRepository,
        InterestInReadSchema,
        InterestOutSchema,
    ]
):
    async def execute(self, *, interests_uuids: list[UUID]):
        async with self.repository as repo:
            interests = await repo.fetch(entry_ids=interests_uuids)
        return TypeAdapter(list[InterestOutSchema]).validate_python(interests)


class ListInterests(
    BaseUseCase[
        InterestReadOnlyRepository,
        InterestInReadSchema,
        InterestOutSchema,
    ]
):
    async def execute(self):
        async with self.repository as repo:
            interests = await repo.list()
        return InterestsOutSchema(
            interests=TypeAdapter(list[InterestOutSchema]).validate_python(interests)
        )
