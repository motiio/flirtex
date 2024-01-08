from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.modules.auth.api.private.internal import JWTAuthFacade

AuthAPI = JWTAuthFacade.create()
CurrentUser = Annotated[UUID, Depends(AuthAPI.auth_user)]
