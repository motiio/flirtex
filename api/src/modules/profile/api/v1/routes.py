from uuid import UUID

from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.modules.auth.application.dependencies.auth import CurrentUser
from src.modules.deck.application.dependencies.filter import CreateFilterService
from src.modules.deck.application.dtos.filter import FilterInCreateDTO
from src.modules.profile.api.v1.schemas import (
    CreateProfileRequestSchema,
    UpdateProfileInterestsRequestSchema,
    UpdateProfileRequestSchema,
)
from src.modules.profile.api.v1.schemas.update_photo_order import (
    UpdatePhotoOrderRequest,
)
from src.modules.profile.application.dependencies import (
    AddProfilePhotoService,
    CreateProfileService,
    DeleteProfilePhotoService,
    DeleteProfileService,
    GetProfileService,
    UpdatePhotoOrderService,
    UpdateProfileService,
    ValidImageFile,
)
from src.modules.profile.application.dtos import (
    CreateProfileInDTO,
    PhotoOutDTO,
    ProfileOutDTO,
    UpdateProfileInDTO,
)
from src.modules.profile.application.dtos.photo import (
    PhotoInCreateDTO,
    PhotoInDeleteDTO,
    UpdatePhotosOrderInDTO,
    UpdatePhotosOrderOutDTO,
)
from src.modules.profile.application.dtos.profile import UpdateProfileOutDTO

profile_router = APIRouter(prefix="/profile")


@profile_router.get(
    "",
    response_model=ProfileOutDTO,
    status_code=HTTP_200_OK,
)
async def get_profile(
    get_profile_service: GetProfileService,
    user_id: CurrentUser,
):
    """
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    profile: ProfileOutDTO = await get_profile_service.execute(owner_id=user_id)

    return profile


@profile_router.post(
    "",
    response_model=ProfileOutDTO,
    status_code=HTTP_201_CREATED,
)
async def create_profile(
    user_id: CurrentUser,
    profile_data: CreateProfileRequestSchema,
    create_profile_service: CreateProfileService,
    filter_service: CreateFilterService,
):
    """
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    profile: ProfileOutDTO = await create_profile_service.execute(
        in_dto=CreateProfileInDTO(
            owner_id=user_id,
            **profile_data.model_dump(),
        )
    )
    default_filter_data = FilterInCreateDTO(
        profile_id=profile.id,
        age_to=profile.age + 5,
        age_from=profile.age - 5,
        looking_gender=profile_data.looking_gender,
        max_distance=10,
    )
    _ = await filter_service.execute(in_dto=default_filter_data)
    return profile


@profile_router.patch(
    "",
    response_model=UpdateProfileOutDTO,
    status_code=HTTP_200_OK,
)
async def update_profile(
    profile_data: UpdateProfileRequestSchema,
    update_profile_service: UpdateProfileService,
    user_id: CurrentUser,
):
    """
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    profile: UpdateProfileOutDTO = await update_profile_service.execute(
        in_dto=UpdateProfileInDTO(
            owner_id=user_id,
            **profile_data.model_dump(),
        )
    )

    return profile


@profile_router.put(
    "/interests",
    status_code=HTTP_200_OK,
    response_model=ProfileOutDTO,
)
async def update_profile_interests(
    new_interests: UpdateProfileInterestsRequestSchema,
    update_profile_service: UpdateProfileService,
    user_id: CurrentUser,
):
    """
    Update profile interests.

    Returns:
        Updated profile.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    profile: ProfileOutDTO = await update_profile_service.execute(
        in_dto=UpdateProfileInDTO(
            owner_id=user_id,
            interests=new_interests.interests,
        )
    )

    return profile


@profile_router.delete(
    "",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_profile(
    delete_profile_service: DeleteProfileService,
    user_id: CurrentUser,
):
    """
    Delete user profile.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    _ = await delete_profile_service.execute(owner_id=user_id)


@profile_router.post(
    "/photo",
    status_code=HTTP_201_CREATED,
    response_model=PhotoOutDTO,
)
async def add_profile_photo(
    photo: ValidImageFile,
    user_id: CurrentUser,
    add_profile_photo_service: AddProfilePhotoService,
):
    created_photo: PhotoOutDTO = await add_profile_photo_service.execute(
        in_dto=PhotoInCreateDTO(user_id=user_id, content=await photo.read())
    )
    return created_photo


@profile_router.delete(
    "/photo/{photo_id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_profile_photo(
    photo_id: UUID,
    user_id: CurrentUser,
    delete_profile_photo_service: DeleteProfilePhotoService,
):
    await delete_profile_photo_service.execute(
        in_dto=PhotoInDeleteDTO(user_id=user_id, photo_id=photo_id)
    )


@profile_router.patch(
    "/photo",
    status_code=HTTP_200_OK,
)
async def update_photo_order(
    displayin_order: UpdatePhotoOrderRequest,
    user_id: CurrentUser,
    update_photo_order_service: UpdatePhotoOrderService,
):
    new_order: UpdatePhotosOrderOutDTO = await update_photo_order_service.execute(
        in_dto=UpdatePhotosOrderInDTO(user_id=user_id, photo_orders=displayin_order.new_order)
    )
    return new_order
