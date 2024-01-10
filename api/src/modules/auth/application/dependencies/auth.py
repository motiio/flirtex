from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.modules.auth.api.private.internal.v1 import AuthAPI

CurrentUser = Annotated[UUID, Depends(AuthAPI.auth_user)]
