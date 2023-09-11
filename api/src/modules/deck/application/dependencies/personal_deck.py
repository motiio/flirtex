from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.deck.application.factories.personal_deck import (
    personal_deck_service_factory,
)

PersonalDeckService = Annotated[IUseCase, Depends(personal_deck_service_factory)]
