from src.core.usecases import IUseCase
from src.modules.profile.application.dtos import (
    PhotoOrderDTO,
    UpdatePhotosOrderInDTO,
    UpdatePhotosOrderOutDTO,
)
from src.modules.profile.application.repositories import (
    IProfilePhotoRepository,
    IProfileRepository,
)
from src.modules.profile.domain.exceptions import (
    ProfileNotFound,
)


class UpdatePhotoOrderUsecase(IUseCase):
    def __init__(
        self,
        *,
        photo_repository: IProfilePhotoRepository,
        profile_repository: IProfileRepository,
    ):
        self._photo_repo: IProfilePhotoRepository = photo_repository
        self._profile_repo: IProfileRepository = profile_repository

    async def execute(self, in_dto: UpdatePhotosOrderInDTO) -> UpdatePhotosOrderOutDTO:
        async with self._photo_repo, self._profile_repo:
            profile = await self._profile_repo.get_by_owner(owner_id=in_dto.user_id)

            if not profile:
                raise ProfileNotFound

            id_to_order_map = {
                item.photo_id: item.displaying_order for item in in_dto.photo_orders
            }

            photos = await self._photo_repo.fetch(
                entities_ids=list(id_to_order_map.keys()),
                profile_id=profile.id,
            )

            for photo in photos:
                photo.set_displaying_order(id_to_order_map[photo.id])
                _ = await self._photo_repo.update(in_entity=photo)

            return UpdatePhotosOrderOutDTO(
                photos=[
                    PhotoOrderDTO(
                        displaying_order=photo.displaying_order, photo_id=photo.id
                    )
                    for photo in photos
                ]
            )
