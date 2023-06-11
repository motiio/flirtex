import asyncio
from http.client import ResponseNotReady
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_206_PARTIAL_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.auth.services import CurrentUser
from src.database.core import DbSession

from src.profile.schemas import UserProfileCreateRequest, UserProfileReadSchema
from src.profile.services import (
    create,
    delete_profile_by_user_id,
    get_profile_by_user_id,
    is_image,
    upload_photo_to_s3,
    get_profil_photos_count,
    create_s3_profile_images_storage,
    delete_s3_profile_images_storage,
)
from src.config.core import settings
from src.profile.models import Profile, ProfilePhoto


profile_router = APIRouter()


@profile_router.post(
    "", status_code=HTTP_201_CREATED, response_model=UserProfileReadSchema
)
async def register_profile(
    *,
    user: CurrentUser,
    db_session: DbSession,
    registration_data: UserProfileCreateRequest,
):
    """
    Register a new profile for the current user.

    Args:
    - registration_data: The profile data to register.
    - user: The current user.
    - db_session: The database session.
    - s3_client: The s3 session.

    Returns:
        The newly created profile.
    """
    profile = await get_profile_by_user_id(db_session=db_session, user_id=user)
    if profile:
        return profile

    profile = await create(
        db_session=db_session,
        profile_data=registration_data,
        owner=user,
    )
    await create_s3_profile_images_storage(profile_id=profile.id)

    return profile


@profile_router.post("/photo", status_code=HTTP_201_CREATED)
async def upload_profilt_photo(
    *,
    user: CurrentUser,
    db_session: DbSession,
    files: list[UploadFile] = File(...),
):
    profile_photos_count = await get_profil_photos_count(
        user_id=user, db_session=db_session
    )
    if len(files) + profile_photos_count > settings.MAX_PROFILE_PHOTOS_COUNT:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "message": f"Максимально допустимое количество файлов - {settings.MAX_PROFILE_PHOTOS_COUNT}"
            },
        )

    file_contents = [await file.read() for file in files]  # Чтение содержимого файлов

    tasks = [is_image(file_content=file_content) for file_content in file_contents]
    results = await asyncio.gather(*tasks)

    response = []
    for idx, (file, is_img) in enumerate(zip(files, results)):
        response_entity = {"filename": file.filename, "is_image": is_img}
        if is_img:
            file_content = file_contents[idx]  # Используем сохраненное содержимое файла
            profile_photo: ProfilePhoto = await upload_photo_to_s3(
                user_id=user,
                db_session=db_session,
                file_content=file_content,
                file_idx=idx,
            )
            response_entity["s3_id"] = profile_photo.id
        response.append(response_entity)
    if any(not entry["is_image"] for entry in response):
        return JSONResponse(
            status_code=HTTP_206_PARTIAL_CONTENT,
            content={
                "message": "Некоторые файлы имеют недопустипый формат. Достпно: [jpeg,png,gif]",
                "files": response,
            },
        )

    return {"files": response}


@profile_router.get("", response_model=UserProfileReadSchema)
async def get_my_profile(
    *,
    user: CurrentUser,
    db_session: DbSession,
):
    """
    Get current user's profile.

    Returns:
        The user's profile.

    Raises:
    - HTTPExceptions: **HTTP_404_NOT_FOUND**. If user's profile wos not found
    """
    profile: UserProfileReadSchema = await get_profile_by_user_id(
        db_session=db_session, user_id=int(user)
    )
    if not profile:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail={"msg": "User profile not found"},
        )
    return profile


@profile_router.patch("", response_model=UserProfileReadSchema, status_code=HTTP_200_OK)
def update_profile(*, user: CurrentUser, db_session: DbSession):
    ...


@profile_router.delete("", status_code=HTTP_200_OK)
async def delete_profile(*, user: CurrentUser, db_session: DbSession):
    deleted_profile: Profile = await delete_profile_by_user_id(
        user_id=user,
        db_session=db_session,
    )
    await delete_s3_profile_images_storage(profile_id=deleted_profile.id)
