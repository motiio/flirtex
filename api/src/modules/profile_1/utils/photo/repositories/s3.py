import datetime

from src.v1.base.repositories.s3 import BaseWriteOnlyS3Repository
from src.v1.config.settings import settings
from src.v1.photo.schemas import PhotoInS3CreateSchema, PhotoInS3UpdateSchema


class PhotoS3Repository(
    BaseWriteOnlyS3Repository[
        PhotoInS3CreateSchema,
        PhotoInS3UpdateSchema,
    ]
):
    async def generate_presigned_url(self, *, key: str):
        expiration = datetime.datetime(2100, 1, 1)
        async with self._s3_session.client("s3", endpoint_url=settings.S3_CLOUD_ENDPOINT) as client:
            presigned_url = await client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self._bucket_name,
                    "Key": key,
                },
                ExpiresIn=(expiration - datetime.datetime.now()).total_seconds(),
            )
        return presigned_url
