from abc import ABCMeta, abstractmethod


class IUseCase(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        ...
