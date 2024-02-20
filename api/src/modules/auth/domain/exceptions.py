from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

InvalidInitData = HTTPException(
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    detail={"msg": "Invalid init datat"},
)
InitDataUserNotFound = HTTPException(
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    detail={"msg": "Invalid init datat"},
)
InvalidJWTToken = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail={"msg": "Invalid authentication credentials"},
)

UserNotFound = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail={"msg": "User not found"},
)
