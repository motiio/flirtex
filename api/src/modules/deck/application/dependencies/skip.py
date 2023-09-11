from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.deck.application.factories import (
    skip_service_factory,
)

SkipService = Annotated[IUseCase, Depends(skip_service_factory)]
