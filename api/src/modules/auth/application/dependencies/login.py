from typing import Annotated

from fastapi import Depends

from core.usecases import IUseCase
from modules.auth.application.factories import (
    telegram_login_service_factory,
)

TelegramLoginService = Annotated[IUseCase, Depends(telegram_login_service_factory)]
