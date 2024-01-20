from typing import Annotated

from fastapi import Depends

from src.core.usecases import IUseCase
from src.modules.notifier.application.factories.action_notifier import (
    action_notification_service_factory,
)

ActionNotifierService = Annotated[IUseCase, Depends(action_notification_service_factory)]
