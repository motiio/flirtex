from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

FilterNotFound = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail={"msg": "Filter not found"},
)

FilterAlreadyExists = HTTPException(
    status_code=HTTP_409_CONFLICT,
    detail={"msg": "Filter already exists"},
)
