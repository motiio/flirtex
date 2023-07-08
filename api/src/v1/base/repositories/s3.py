from typing import Generic, TypeVar

from sqlalchemy import except_
from sqlalchemy.orm import with_parent

from src.v1.config.s3 import S3Session
from src.v1.config.settings import settings
from src.v1.base.exceptions import DoesNotExists, AlreadyExists
from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError


from src.v1.base.schemas import BaseS3Schema
from src.v1.base.aio import AsyncContextManagerRepository
from src.v1.base.interfaces import IReadOnlyRepository, IWriteOnlyRepository


IN_S3_CREATE_SCHEMA = TypeVar("IN_S3_CREATE_SCHEMA", bound=BaseS3Schema)
IN_S3_UPDATED_SCHEMA = TypeVar("IN_S3_UPDATED_SCHEMA", bound=BaseS3Schema)


class BaseWriteOnlyS3Repository(
    IWriteOnlyRepository,
    Generic[IN_S3_CREATE_SCHEMA, IN_S3_UPDATED_SCHEMA],
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

    async def delete(self, *, key: str) -> ServiceResource:
        is_exists = await self._is_exists(key=key)
        if not is_exists:
            raise DoesNotExists
        async with self._s3_resource as s3:
            bucket = await s3.Bucket(self._bucket_name)
            obj = bucket.Object(key)
            await obj.delete()
            return obj

    async def update(self, *, in_schema: IN_S3_UPDATED_SCHEMA) -> None:
        ...

    async def commit(self):
        pass


class BaseReadOnlyS3Repository(
    IReadOnlyRepository,
    AsyncContextManagerRepository,
    Generic[IN_S3_CREATE_SCHEMA],
):
    async def __init__(self, *, s3_session: S3Session, bucket_name: str):
        self._s3_session = s3_session.resource(
            "s3", endpoint_url=settings.S3_CLOUD_ENDPOINT
        )
        self._bucket = await self._s3_session.Bucket(bucket_name)  # type: ignore

    async def __aenter__(self):
        return await self._s3_session.__aenter__()

    async def __aexit__(self, exc_type, exc, tb):
        return await self._s3_session.__aexit__(exc_type, exc, tb)

    async def get(self, *, key: str) -> ServiceResource:
        is_exists = await self._is_exists(key=key)
        if not is_exists:
            raise DoesNotExists
        obj = self._bucket.Object(key)
        return obj

    async def _is_exists(self, *, key: str) -> bool:
        obj = self._bucket.Object(key)
        is_exists = await obj.exists()
        return is_exists

    async def commit(self):
        pass
