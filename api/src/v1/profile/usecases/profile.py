from typing import Iterable
from src.v1.config.usecases import BaseUseCase
from src.v1.profile.models import Interest
from src.v1.profile.repositories.profile import ProfileRepository
from src.v1.profile.schemas.profile import ProfileInCreateSchema, ProfileOutSchema


class GetOrCreateProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutSchema,
    ]
):
    async def execute(
        self, *, profile_data: ProfileInCreateSchema, interests: list[Interest]
    ):
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=profile_data.owner_id)
            if not profile:
                profile = await repo.create(in_schema=profile_data, interests=interests)
        return ProfileOutSchema.model_validate(profile)
