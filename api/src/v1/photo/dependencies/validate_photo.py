from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from src.v1.config.settings import settings
from PIL import Image
from src.v1.photo.exceptions import InvalidPhotoSize, InvalidPhotoType
from typing import Annotated


def _check_is_image(photo: UploadFile):
    image_data_b = photo.file.read()
    if image_data_b[:4] not in settings.ACCEPTED_PHOTO_TYPES_B:
        return False
    photo.file.seek(0)
    return True


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
