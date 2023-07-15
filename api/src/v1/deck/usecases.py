from uuid import UUID
from src.v1.base.usecases import BaseUseCase
from src.v1.deck.repositories.db import (
    LikeRepository,
    MatchRepository,
    SaveRepository,
    SkipRepository,
)
from src.v1.deck.schemas import (
    LikeInCreateSchema,
    MatchInCreateSchema,
    SaveInCreateSchema,
    SkipInCreateSchema,
)


class CreateLike(
    BaseUseCase[
        LikeRepository,
        LikeInCreateSchema,
        None,
    ]
):
    async def execute(self, *, in_schema: LikeInCreateSchema):
        async with self.repository as repo:
            await repo.create(in_schema=in_schema)


class CreateSkip(
    BaseUseCase[
        SkipRepository,
        SkipInCreateSchema,
        None,
    ]
):
    async def execute(self, *, in_schema: SkipInCreateSchema):
        async with self.repository as repo:
            await repo.create(in_schema=in_schema)


class CreateSave(
    BaseUseCase[
        SaveRepository,
        SaveInCreateSchema,
        None,
    ]
):
    async def execute(self, *, in_schema: SaveInCreateSchema):
        async with self.repository as repo:
            await repo.create(in_schema=in_schema)


class CreateMatch(
    BaseUseCase[
        MatchRepository,
        MatchInCreateSchema,
        None,
    ]
):
    async def execute(self, *, in_schema: MatchInCreateSchema):
        async with self.repository as repo:
            await repo.create(in_schema=in_schema)


class CheckMatch(
    BaseUseCase[
        LikeRepository,
        None,
        None,
    ]
):
    async def execute(self, *, source_profile: UUID, target_profile: UUID):
        async with self.repository as repo:
            result = await repo.check_like_from_target_profile(
                source_profile=source_profile, target_profile=target_profile
            )
            if result:
                return True
            return False


class DeleteMutualLikes(
    BaseUseCase[
        LikeRepository,
        None,
        None,
    ]
):
    async def execute(self, *, source_profile: UUID, target_profile: UUID):
        async with self.repository as repo:
            await repo.delete_mutual_like(
                source_profile=source_profile, target_profile=target_profile
            )
