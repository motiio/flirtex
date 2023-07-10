from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

InvalidInitData = HTTPException(
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    detail=[{"msg": "Invalid init datat"}],
)

InvalidToken = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
)
