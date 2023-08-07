from abc import abstractmethod
from typing import Generic, List
from uuid import UUID

from src.config.s3 import S3Session
from src.config.settings import settings
from src.core.repositories import IS3Repository
from src.core.types import IN_S3_DTO, OUT_DTO


class BaseS3Repository(
    IS3Repository,
    Generic[
        IN_S3_DTO,
        OUT_DTO,
    ],
):
    def __init__(self, *, s3_session: S3Session, endpoint_url: str = settings.S3_CLOUD_ENDPOINT):
        self._s3_session = s3_session
        self._endpoint_url = endpoint_url

    @property
    @abstractmethod
    def _bucket_name(self) -> str:
        ...

    async def create(self, *, in_dto: IN_S3_DTO) -> None:
        async with self._s3_session.resource("s3", endpoint_url=settings.S3_CLOUD_ENDPOINT) as s3:
            bucket = await s3.Bucket(self._bucket_name)
            await bucket.put_object(Key=in_dto.key, Body=in_dto.content)  # type: ignore

    async def delete(self, *, key: UUID) -> None:
        async with self._s3_session.resource("s3", endpoint_url=settings.S3_CLOUD_ENDPOINT) as s3:
            bucket = await s3.Bucket(self._bucket_name)
            await bucket.objects.filter(Prefix=key).delete()

    async def get(self, *, entity_id) -> OUT_DTO | None:
        ...

    async def list(self) -> List[OUT_DTO] | None:
        ...

    async def fetch(self, *, entity_ids: List[UUID]) -> List[OUT_DTO] | None:
        ...

    async def update(self, *, in_entity: IN_S3_DTO) -> List[OUT_DTO]:
        ...

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            # TODO добавить логирование
            await self.rollback()
        await self.commit()
