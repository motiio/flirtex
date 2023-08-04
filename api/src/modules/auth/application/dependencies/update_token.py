from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.auth.application.factories.update_token import (
    update_token_service_factory,
)

UpdateTokenService = Annotated[IUseCase, Depends(update_token_service_factory)]
