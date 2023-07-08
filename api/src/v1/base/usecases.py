from abc import ABCMeta, abstractmethod
from typing import Generic, Optional, TypeVar, Union

from src.v1.base.repositories.db import (
    BaseReadOnlyRepository,
    BaseWriteOnlyRepository,
)
from src.v1.base.repositories.s3 import (
    BaseReadOnlyS3Repository,
    BaseWriteOnlyS3Repository,
)
from src.v1.base.schemas import BaseSchema, BaseS3Schema

REPOSITORY = TypeVar(
    "REPOSITORY",
    bound=Optional[
        Union[
            BaseReadOnlyRepository,
            BaseWriteOnlyRepository,
            BaseWriteOnlyS3Repository,
            BaseReadOnlyS3Repository,
        ]
    ],
)
IN_SCHEMA = TypeVar("IN_SCHEMA", bound=Union[BaseSchema, BaseS3Schema])
OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=Union[BaseSchema, BaseS3Schema])


class BaseUseCase(Generic[REPOSITORY, IN_SCHEMA, OUT_SCHEMA], metaclass=ABCMeta):
    repository: REPOSITORY

    def __init__(self, repository: REPOSITORY) -> None:
        self.repository = repository

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
