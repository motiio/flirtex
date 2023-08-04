from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.common.application.factories import (
    list_interests_service_factory,
)

ListInterestsService = Annotated[IUseCase, Depends(list_interests_service_factory)]
