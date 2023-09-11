from src.core.usecases import IUseCase
from src.modules.profile.application.dtos import (
    CreateProfileInDTO,
    ProfileOutDTO,
)
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.domain.entities import Profile
from src.modules.profile.domain.exceptions import ProfileAlreadyExists


class CreateProfileUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
    ):
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, in_dto: CreateProfileInDTO) -> ProfileOutDTO:
        async with self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(
                owner_id=in_dto.owner_id
            )
            if existent_profile:
                raise ProfileAlreadyExists

            created_profile = Profile.create(**in_dto.model_dump(exclude={"interests"}))
            created_profile.put_location(location=in_dto.location)
            profile = await self._profile_repo.create(
                in_entity=created_profile, interests_ids=in_dto.interests
            )
            return ProfileOutDTO(**profile.model_dump())
