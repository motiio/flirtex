from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.profile.application.factories import (
    add_profile_photo_service_factory,
)

AddProfilePhotoService = Annotated[IUseCase, Depends(add_profile_photo_service_factory)]
