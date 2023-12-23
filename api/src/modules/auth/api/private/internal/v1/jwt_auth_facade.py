from fastapi import Depends
from fastapi.exceptions import HTTPException

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uuid import UUID

from starlette.status import HTTP_401_UNAUTHORIZED
from src.modules.auth.application.utils import jwt


security = HTTPBearer()


class JWTAuthFacade:
    @staticmethod
    def _get_user(*, jwt_token: str) -> UUID | None:
        _, data = jwt.check_token_signature(token=jwt_token)
        user_id: str = data["sub"]
        if user_id is None:
            return None
        return UUID(user_id)

    @staticmethod
    def auth_user(
        *,
        auth: HTTPAuthorizationCredentials = Depends(security),
    ) -> UUID:
        token = auth.credentials
        uuid = JWTAuthFacade._get_user(jwt_token=token)
        if not uuid:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials"
            )
        return uuid
