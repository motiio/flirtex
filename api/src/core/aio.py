from abc import ABCMeta, abstractmethod


class IAsyncContextManagerRepository(metaclass=ABCMeta):
    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, tb):
        ...
