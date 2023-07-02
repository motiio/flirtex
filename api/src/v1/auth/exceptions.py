from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

InvalidInitData = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail=[{"msg": "Invalid init datat"}],
)

InvalidToken = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
)
