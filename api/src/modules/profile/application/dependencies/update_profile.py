from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.profile.application.factories import (
    update_profile_service_factory,
)

UpdateProfileService = Annotated[IUseCase, Depends(update_profile_service_factory)]
