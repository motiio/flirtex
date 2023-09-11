from abc import ABCMeta, abstractmethod

from src.core.types import OUT_DTO


class IUseCase(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> OUT_DTO:
        ...
