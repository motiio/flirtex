from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
)

from src.v1.config.settings import settings

MaxPhotoLimit = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail={"msg": "The limit on the number of profile photos has been reached"},
)
PhotoAlreadyExists = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail={"msg": "This photo has already been uploaded"},
)
InvalidPhotoType = HTTPException(
    status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail={"msg": "invalid image format, available formats: [jpeg, jpg]"},
)
InvalidPhotoSize = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail={"msg": f"Photo size too big. Available size {settings.MAX_PROFILE_PHOTO_SIZE_B}"},
)
PhotoNotFound = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail={"msg": "Photo not found"},
)
