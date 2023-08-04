from io import BytesIO
from typing import Annotated

from fastapi import Depends, UploadFile
from PIL import Image

from src.v1.config.settings import settings
from src.v1.photo.exceptions import InvalidPhotoSize, InvalidPhotoType


def _check_is_image(photo: UploadFile):
    image_data_b = photo.file.read()
    try:
        image = Image.open(BytesIO(image_data_b))
        image.verify()
        return image.format in settings.ACCEPTED_PHOTO_TYPES
    except (IOError, SyntaxError, ValueError):
        return False
    finally:
        photo.file.seek(0)


def _check_size(photo: UploadFile):
    image_data_b = photo.file.read()
    if len(image_data_b) > settings.MAX_PROFILE_PHOTO_SIZE_B:
        return False
    photo.file.seek(0)
    return True


def validate_photo(photo: UploadFile):
    if not _check_size(photo):
        return InvalidPhotoSize
    if not _check_is_image(photo):
        raise InvalidPhotoType
    return photo


ValidImageFile = Annotated[UploadFile, Depends(validate_photo)]
