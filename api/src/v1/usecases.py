from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Union

from src.v1.repositories import (
    BaseReadOnlyRepository,
    BaseRepository,
    BaseWriteOnlyRepository,
)
from src.v1.schemas import BaseSchema

REPOSITORY = TypeVar(
    "REPOSITORY",
    bound=Union[BaseRepository, BaseReadOnlyRepository, BaseWriteOnlyRepository],
)
IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=BaseSchema)


class BaseUseCase(Generic[REPOSITORY, IN_SCHEMA, OUT_SCHEMA], metaclass=ABCMeta):
    repository: REPOSITORY

    def __init__(self, repository: REPOSITORY) -> None:
        self.repository = repository

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
