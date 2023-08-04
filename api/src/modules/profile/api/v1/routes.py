from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.modules.auth.application.dependencies.auth import CurrentUser
from src.modules.profile.api.v1.schemas import (
    CreateProfileRequestSchema,
    UpdateProfileInterestsRequestSchema,
    UpdateProfileRequestSchema,
)
from src.modules.profile.application.dependencies import (
    CreateProfileService,
    DeleteProfileService,
    GetProfileService,
    UpdateProfileService,
)
from src.modules.profile.application.dtos import (
    CreateProfileInDTO,
)
from src.modules.profile.application.dtos.profile import (
    ProfileOutDTO,
    UpdateProfileInDTO,
)

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
)
async def update_profile_interests(
    new_interests: UpdateProfileInterestsRequestSchema,
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
    Login user.

    Returns:
        The user's **access token** and **refresh token**.

    - HTTPExceptions: **HTTP_401_UNAUTHORIZED**. If user's initData is invalid
    """
    await delete_profile_service.execute(owner_id=user_id)
