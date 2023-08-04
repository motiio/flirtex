from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.auth.application.factories import (
    telegram_login_service_factory,
)

TelegramLoginService = Annotated[IUseCase, Depends(telegram_login_service_factory)]
