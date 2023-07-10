from typing import Generic, TypeVar

from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

from src.v1.base.aio import AsyncContextManagerRepository
from src.v1.base.exceptions import AlreadyExists, DoesNotExists
from src.v1.base.interfaces import IReadOnlyRepository, IWriteOnlyRepository
from src.v1.base.schemas import BaseS3Schema
from src.v1.config.s3 import S3Session
from src.v1.config.settings import settings

IN_S3_CREATE_SCHEMA = TypeVar("IN_S3_CREATE_SCHEMA", bound=BaseS3Schema)
IN_S3_UPDATED_SCHEMA = TypeVar("IN_S3_UPDATED_SCHEMA", bound=BaseS3Schema)


class BaseWriteOnlyS3Repository(
    IWriteOnlyRepository,
    Generic[
        IN_S3_CREATE_SCHEMA,
        IN_S3_UPDATED_SCHEMA,
    ],
):
    def __init__(self, *, s3_session: S3Session, bucket_name: str):
        self._s3_session = s3_session
        self._s3_resource = s3_session.resource(
            "s3", endpoint_url=settings.S3_CLOUD_ENDPOINT
        )
        self._bucket_name = bucket_name

    async def _is_exists(self, *, key: str) -> bool:
        async with self._s3_session.client(
            "s3", endpoint_url=settings.S3_CLOUD_ENDPOINT
        ) as client:
            try:
                _ = await client.head_object(Bucket=self._bucket_name, Key=key)
            except ClientError:
                return False
            return True

    async def create(self, *, in_schema: IN_S3_CREATE_SCHEMA) -> None:
        is_exists = await self._is_exists(key=in_schema.key)
        if is_exists:
            raise AlreadyExists
        async with self._s3_resource as s3:
            bucket = await s3.Bucket(self._bucket_name)
            await bucket.put_object(Key=in_schema.key, Body=in_schema.content)  # type: ignore

    async def delete(self, *, key: str) -> None:
        is_exists = await self._is_exists(key=key)
        if not is_exists:
            raise DoesNotExists
        async with self._s3_resource as s3:
            bucket = await s3.Bucket(self._bucket_name)
            await bucket.objects.filter(Prefix=key).delete()

    async def update(self, *, in_schema: IN_S3_UPDATED_SCHEMA) -> None:
        ...

    async def commit(self):
        pass
