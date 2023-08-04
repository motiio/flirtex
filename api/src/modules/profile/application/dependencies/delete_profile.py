from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.profile.application.factories import (
    delete_profile_service_factory,
)

DeleteProfileService = Annotated[IUseCase, Depends(delete_profile_service_factory)]
