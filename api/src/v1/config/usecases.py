from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from src.v1.config.repositories import BaseRepository
from src.v1.config.schemas import BaseSchema

REPOSITORY = TypeVar("REPOSITORY", bound=BaseRepository)
IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=BaseSchema)


class BaseUseCase(Generic[REPOSITORY, IN_SCHEMA, OUT_SCHEMA], metaclass=ABCMeta):
    repository: REPOSITORY

    def __init__(self, repository: REPOSITORY) -> None:
        self.repository = repository

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
