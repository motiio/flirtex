from typing import Annotated

from fastapi import Depends

from core.usecases import IUseCase
from auth.application.factories.update_token import (
    update_token_service_factory,
)

UpdateTokenService = Annotated[IUseCase, Depends(update_token_service_factory)]
