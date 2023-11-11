from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.deck.application.factories import (
    like_reactions_service_factory,
)

LikeReactionsService = Annotated[IUseCase, Depends(like_reactions_service_factory)]
