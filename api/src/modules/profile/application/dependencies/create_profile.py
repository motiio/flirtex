from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.profile.application.factories import (
    create_profile_service_factory,
)

CreateProfileService = Annotated[IUseCase, Depends(create_profile_service_factory)]
