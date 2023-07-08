from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from src.v1.config.settings import settings
from PIL import Image
from src.v1.photo.exceptions import InvalidPhotoType


async def check_is_image(photo: UploadFile):
    image_data_b = photo.file.read()
    if image_data[:4] not in settings.ACCEPTED_PHOTO_TYPES_B:
        return False
    return True


def validate_photo(photo: UploadFile):
    image_data_b = photo.file.read()
    if len(image_data_b) > settings.MAX_PROFILE_PHOTO_SIZE_B:
        raise InvalidPhotoSize
