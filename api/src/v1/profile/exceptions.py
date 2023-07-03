from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

ProfileNotFound = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail={"msg": "User profile not found"},
)
