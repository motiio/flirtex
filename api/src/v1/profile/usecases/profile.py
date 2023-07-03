from uuid import UUID

from pydantic import TypeAdapter
from src.v1.profile.exceptions import ProfileNotFound, ProfileAlreadyExists
from src.v1.profile.schemas.interest import InterestOutSchema, InterestsOutSchema
from src.v1.usecases import BaseUseCase
from src.v1.profile.models import Interest
from src.v1.profile.repositories.profile import ProfileRepository
from src.v1.profile.schemas.profile import (
    ProfileInCreateSchema,
    ProfileOutCreateSchema,
    ProfileInUpdateSchema,
    ProfileOutReadSchema,
)


class CreateProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(
        self,
        *,
        profile_data: ProfileInCreateSchema,
    ):
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=profile_data.owner_id)
            if profile:
                raise ProfileAlreadyExists
            profile = await repo.create(in_schema=profile_data)
        return ProfileOutCreateSchema.model_validate(profile)


class GetUserProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(self, *, user_id: UUID):
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=user_id)
            if not profile:
                raise ProfileNotFound
            return ProfileOutReadSchema.model_validate(profile)


class UpdateUserProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(self, *, profile_data: ProfileInUpdateSchema):
        async with self.repository as repo:
            new_profile = await repo.update_by_owner(
                in_schema=profile_data,
                owner_id=profile_data.owner_id,
            )
            return ProfileOutReadSchema.model_validate(new_profile)


class DeleteUserProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(
        self,
        *,
        profile_owner: UUID,
    ) -> None:
        async with self.repository as repo:
            await repo.delete_by_owner(owner_id=profile_owner)


class CreateProfileInterests(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(
        self, *, owner_id: UUID, interests: list[Interest]
    ) -> InterestsOutSchema:
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=owner_id)
            profile.interests = interests
            return InterestsOutSchema(
                interests=TypeAdapter(list[InterestOutSchema]).validate_python(
                    profile.interests
                )
            )
