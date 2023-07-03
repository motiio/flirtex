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
