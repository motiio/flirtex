from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.profile.application.factories import (
    delete_profile_photo_service_factory,
)

DeleteProfilePhotoService = Annotated[
    IUseCase, Depends(delete_profile_photo_service_factory)
]
