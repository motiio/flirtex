from uuid import UUID
from typing import Annotated
from fastapi import Depends
from auth.api.private.internal import JWTAuthFacade

CurrentUser = Annotated[UUID, Depends(JWTAuthFacade.auth_user)]
