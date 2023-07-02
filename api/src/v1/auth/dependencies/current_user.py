from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from src.v1.auth.models import User
from src.v1.auth.utils import jwt

security = HTTPBearer()


def _get_current_user(
    *,
    auth: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    try:
        token = auth.credentials
        _, data = jwt.check_token_signature(token=token)
        user_id: str = data["sub"]
        if user_id is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return UUID(user_id)
    except HTTPException:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from None


CurrentUser = Annotated[User, Depends(_get_current_user)]
