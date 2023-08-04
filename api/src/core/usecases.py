from abc import ABCMeta, abstractmethod
from typing import Generic

from src.core.types import IN_DTO, OUT_DTO


class IUseCase(Generic[IN_DTO, OUT_DTO], metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> OUT_DTO:
        ...
