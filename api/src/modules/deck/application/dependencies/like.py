from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.deck.application.factories import (
    like_service_factory,
)

LikeService = Annotated[IUseCase, Depends(like_service_factory)]
