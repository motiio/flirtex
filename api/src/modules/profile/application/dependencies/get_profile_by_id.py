from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.profile.application.factories import (
    get_profile_by_id_service_factory,
)

GetProfileByIdService = Annotated[IUseCase, Depends(get_profile_by_id_service_factory)]
