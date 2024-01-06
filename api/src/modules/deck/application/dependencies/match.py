from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.deck.application.factories import matches_service_factory

MatchService = Annotated[IUseCase, Depends(matches_service_factory)]
