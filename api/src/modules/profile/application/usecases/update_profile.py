from src.core.usecases import IUseCase
from src.modules.profile.application.dtos import (
    ProfileOutDTO,
    UpdateProfileInDTO,
)
from src.modules.profile.application.repositories import (
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import ProfileNotFound


class UpdateProfileUsecase(IUseCase):
    def __init__(
        self,
        *,
        profile_repository: IProfileRepository,
    ):
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, in_dto: UpdateProfileInDTO) -> ProfileOutDTO:
        async with self._profile_repo:
            existent_profile = await self._profile_repo.get_by_owner(owner_id=in_dto.owner_id)
            if not existent_profile:
                raise ProfileNotFound

            existent_profile.bio = in_dto.bio or existent_profile.bio
            existent_profile.location = in_dto.location or existent_profile.location

            profile = await self._profile_repo.update(
                in_entity=existent_profile, interests_ids=in_dto.interests
            )

            return ProfileOutDTO(**profile.model_dump())
