from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import delete

from src.v1.profile.exceptions import ProfileAlreadyExists, ProfileNotFound
from src.v1.profile.models import Interest
from src.v1.profile.repositories.db import ProfileRepository
from src.v1.interest.schemas import InterestOutSchema, InterestsOutSchema
from src.v1.profile.schemas import (
    ProfileInCreateSchema,
    ProfileInUpdateSchema,
    ProfileOutCreateSchema,
    ProfileOutReadSchema,
)
from src.v1.base.usecases import BaseUseCase


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
    async def execute(
        self,
        *,
        user_id: UUID,
    ):
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=user_id)
            if not profile:
                raise ProfileNotFound
            return ProfileOutReadSchema.model_validate(profile)


class UpdateProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(
        self,
        *,
        profile_data: ProfileInUpdateSchema,
    ):
        async with self.repository as repo:
            new_profile = await repo.update_by_owner(
                in_schema=profile_data,
                owner_id=profile_data.owner_id,
            )
            if new_profile is None:
                raise ProfileNotFound
            return ProfileOutReadSchema.model_validate(new_profile)


class DeleteProfile(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(
        self,
        *,
        profile_id: UUID,
    ) -> None:
        async with self.repository as repo:
            await repo.delete(entry_id=profile_id)


class CreateProfileInterests(
    BaseUseCase[
        ProfileRepository,
        ProfileInCreateSchema,
        ProfileOutReadSchema,
    ]
):
    async def execute(
        self,
        *,
        owner_id: UUID,
        interests: list[Interest],
    ) -> InterestsOutSchema:
        async with self.repository as repo:
            profile = await repo.get_by_owner(owner_id=owner_id)
            if not profile:
                raise ProfileNotFound
            profile.interests = interests
            return InterestsOutSchema(
                interests=TypeAdapter(list[InterestOutSchema]).validate_python(
                    profile.interests
                )
            )
