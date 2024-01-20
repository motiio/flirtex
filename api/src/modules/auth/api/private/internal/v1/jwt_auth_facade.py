from typing import Type
from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from src.modules.auth.application.utils import jwt
from src.modules.auth.infrastructure.models import UserORM

security = HTTPBearer()


class JWTAuthFacade:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(JWTAuthFacade, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def _get_user(
        cls,
        *,
        jwt_token: str,
    ) -> UUID | None:
        _, data = jwt.check_token_signature(token=jwt_token)
        user_id: str = data["sub"]
        if user_id is None:
            return None
        return UUID(user_id)

    @classmethod
    def auth_user(
        cls,
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

    @property
    def user_table(self) -> Type[UserORM]:
        return UserORM

    @classmethod
    def create(cls) -> "JWTAuthFacade":
        return cls()

