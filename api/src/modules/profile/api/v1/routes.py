from uuid import UUID
from fastapi import APIRouter, UploadFile
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.modules.auth.application.dependencies.auth import CurrentUser
from src.modules.profile.api.v1.schemas import (
    CreateProfileRequestSchema,
    UpdateProfileInterestsRequestSchema,
    UpdateProfileRequestSchema,
)
from src.modules.profile.application.dependencies import (
    AddProfilePhotoService,
    CreateProfileService,
    DeleteProfileService,
    GetProfileService,
    UpdateProfileService,
    ValidImageFile,
)
from src.modules.profile.application.dtos import (
    CreateProfileInDTO,
    PhotoOutDTO,
    ProfileOutDTO,
    UpdateProfileInDTO,
)
from src.modules.profile.application.dtos.photo import PhotoInCreateDTO

profile_router = APIRouter(prefix="/profile")


@profile_router.get(
    "",
    response_model=ProfileOutDTO,
    status_code=HTTP_201_CREATED,
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
    profile = await get_profile_service.execute(owner_id=user_id)

    return profile


@profile_router.post(
    "",
    response_model=ProfileOutDTO,
    status_code=HTTP_201_CREATED,
)
async def create_profile(
    profile_data: CreateProfileRequestSchema,
    create_profile_service: CreateProfileService,
    user_id: CurrentUser,
):
    """
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    profile = await create_profile_service.execute(
        in_dto=CreateProfileInDTO(
            owner_id=user_id,
            **profile_data.model_dump(),
        )
    )

    return profile


@profile_router.patch(
    "",
    response_model=ProfileOutDTO,
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
    profile = await update_profile_service.execute(
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
    profile = await update_profile_service.execute(
        in_dto=UpdateProfileInDTO(
            owner_id=user_id,
            interests=new_interests.interests,
        )
    )

    return profile


@profile_router.delete(
    "",
    status_code=HTTP_200_OK,
)
async def delete_profile(
    delete_profile_service: DeleteProfileService,
    user_id: CurrentUser,
):
    """
    Delete user profile.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    await delete_profile_service.execute(owner_id=user_id)


@profile_router.post(
    "/photo",
    status_code=HTTP_200_OK,
    response_model=PhotoOutDTO,
)
async def add_profile_photo(
    photo: ValidImageFile,
    user_id: CurrentUser,
    add_profile_photo_service: AddProfilePhotoService,
):
    created_photo = await add_profile_photo_service.execute(
        in_dto=PhotoInCreateDTO(user_id=user_id, content=await photo.read())
    )
    return created_photo


@profile_router.delete(
    "/photo",
    status_code=HTTP_200_OK,
    # response_model=PhotoOutDTO,
)
async def delete_profile_photo(
    photo_id: UUID,
    user_id: CurrentUser,
    delete_profile_photo_service: DeleteProfilePhotoService,
):
    await delete_profile_photo_service.execute(
        in_dto=PhotoInDeleteDTO(user_id=user_id, photo_id=photo_id)
    )
