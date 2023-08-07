from io import BytesIO
from typing import Annotated

from fastapi import Depends, File, HTTPException, UploadFile, status
from PIL import Image

from src.config.settings import settings


async def _check_is_image(photo: UploadFile) -> bool:
    image_data_b = await photo.read()
    try:
        image = Image.open(BytesIO(image_data_b))
        image.verify()
        return image.format in settings.ACCEPTED_PHOTO_TYPES
    except (IOError, SyntaxError, ValueError):
        return False
    finally:
        photo.file.seek(0)


async def _check_size(photo: UploadFile) -> bool:
    image_data_b = await photo.read()
    if len(image_data_b) > settings.MAX_PROFILE_PHOTO_SIZE_B:
        return False
    photo.file.seek(0)
    return True


async def validate_photo(photo: UploadFile = File(...)) -> UploadFile:
    size_check = await _check_size(photo)
    image_check = await _check_is_image(photo)

    if not size_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid photo size",
        )

    if not image_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid photo type",
        )

    return photo


ValidImageFile = Annotated[UploadFile, Depends(validate_photo)]
