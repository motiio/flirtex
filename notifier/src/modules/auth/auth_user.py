from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from jose.exceptions import JWKError
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config.settings import settings

security = HTTPBearer()


def check_token_signature(
    *,
    token: str,
    secret: str = settings.JWT_SECRET,
) -> tuple[str, dict]:
    try:
        data = jwt.decode(token, secret, algorithms=["HS256"])
    except (JWKError, JWTError):
        raise JWTError from None
    else:
        return token, data


def _get_user(
    *,
    jwt_token: str,
) -> UUID | None:
    _, data = check_token_signature(token=jwt_token)
    user_id: str = data["sub"]
    if user_id is None:
        return None
    return UUID(user_id)


def auth_user(
    *,
    auth: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    token = auth.credentials
    uuid = _get_user(jwt_token=token)
    if not uuid:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return uuid
