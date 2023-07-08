from abc import ABCMeta, abstractmethod


class AsyncContextManagerRepository(metaclass=ABCMeta):
    @abstractmethod
    async def commit(self):
        ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.commit()
