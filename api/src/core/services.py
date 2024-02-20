from abc import ABCMeta, abstractmethod


class IService(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, *args, **kwargs): ...
