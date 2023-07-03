from typing import Optional
from uuid import UUID

from src.v1.profile.exceptions import ProfileNotFound
from src.v1.usecases import BaseUseCase
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
        self,
        *,
        profile_data: ProfileInCreateSchema,
        interests: Optional[list[Interest]],
    ):
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=profile_data.owner_id)
            if not profile:
                profile = await repo.create(
                    in_schema=profile_data,
                    interests=interests or [],
                )
        return ProfileOutSchema.model_validate(profile)


class GetUserProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutSchema,
    ]
):
    async def execute(self, *, user_id: UUID):
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=user_id)
            if not profile:
                raise ProfileNotFound
            return ProfileOutSchema.model_validate(profile)


class UpdateUserProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutSchema,
    ]
):
    async def execute(
        self,
        *,
        profile_data,
        interests,
    ):
        async with self.repository as repo:
            new_profile = await repo.update(in_schema=profile_data, interests=interests)
            return ProfileOutSchema.model_validate(new_profile)


class DeleteUserProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutSchema,
    ]
):
    async def execute(
        self,
        *,
        profile_owner: UUID,
    ) -> None:
        async with self.repository as repo:
            await repo.delete_by_owner(owner_id=profile_owner)


# class ListProfileInterestsToUpdate(
#     BaseUseCase[
#         ProfileRepository,
#         ProfileInCreateSchema,
#         ProfileOutSchema,
#     ]
# ):
# async execute(self, *, profile_data,) -> list[InterestOutSchema]:
#     async self.repository as repo:
#         if profile_data.interests is None:
#             interests = repo.get_by_owner()
#
#
