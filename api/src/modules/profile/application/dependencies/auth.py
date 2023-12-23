from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.modules.auth.api.private.internal import JWTAuthFacade

CurrentUser = Annotated[UUID, Depends(JWTAuthFacade.auth_user)]
