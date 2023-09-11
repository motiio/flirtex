from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.deck.application.factories import (
    create_filter_service_factory,
    get_filter_service_factory,
    update_filter_service_factory,
)

CreateFilterService = Annotated[IUseCase, Depends(create_filter_service_factory)]
UpdateFilterService = Annotated[IUseCase, Depends(update_filter_service_factory)]
GetFilterService = Annotated[IUseCase, Depends(get_filter_service_factory)]
