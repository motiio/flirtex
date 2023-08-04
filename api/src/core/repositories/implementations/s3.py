from typing import Generic

from src.core.repositories import IS3Repository
from src.core.types import BUCKET_NAME, IN_DTO, OUT_DTO
from src.v1.config.s3 import S3Session
from src.v1.config.settings import settings


class BaseS3Repository(
    IS3Repository,
    Generic[
        IN_DTO,
        OUT_DTO,
        BUCKET_NAME,
    ],
):
    def __init__(self, *, s3_session: S3Session, endpoint_url: str = settings.S3_CLOUD_ENDPOINT):
        self._s3_session = s3_session
        self._endpoint_url = endpoint_url

    @property
    async def _bucket(self):
        async with self._s3_session.resource("s3", endpoint_url=self._endpoint_url) as s3:
            bucket = await s3.Bucket(BUCKET_NAME)
        return bucket

    async def create(self, *, created_dto: IN_DTO) -> OUT_DTO:
        await self._s3_session.client(
            "s3",
            endpoint_url=settings.S3_CLOUD_ENDPOINT,
        ).upload_fileobj(
            **created_dto.model_dump(),
            Bucket=BUCKET_NAME,
        )  # type: ignore
        return self._out_dto(**created_dto)

    async def delete(self, *, key: str) -> OUT_DTO:
        async with self._s3_session.resource("s3", endpoint_url=settings.S3_CLOUD_ENDPOINT):
            deleted_object = await self._bucket.objects.filter(Prefix=key)
            await deleted_object.delete()
            return self._out_dto(**deleted_object)

    async def update(self, *, updated_dto: IN_DTO) -> OUT_DTO:
        ...

    async def commit(self):
        pass

    async def rollback(self):
        pass
