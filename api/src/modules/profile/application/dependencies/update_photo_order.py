from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.profile.application.factories import (
    update_photo_order_service_factory,
)

UpdatePhotoOrderService = Annotated[IUseCase, Depends(update_photo_order_service_factory)]
