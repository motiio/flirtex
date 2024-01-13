from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
)

InvalidJWTToken = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail={"msg": "Invalid authentication credentials"},
)
