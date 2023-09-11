from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

ProfileNotFound = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail={"msg": "User profile not found"},
)

ProfileAlreadyExists = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail={"msg": "User profile already exists"},
)

PhotoAlreadyExists = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail={"msg": "The photo already exists"},
)

PhotosLimit = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail={"msg": "The limit of the number of photos has been reached. Min = 1, max = 7"},
)

InvalidOrderList = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail={"msg": "Invalid order list"},
)

InvalidLongitude = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail={"msg": "Invalid longitude. Must by -180 < value < 180"},
)

InvalidLatitude = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail={"msg": "Invalid latitude. Must by -90 < value < 90"},
)
