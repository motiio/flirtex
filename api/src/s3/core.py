from typing import Annotated

import aioboto3
import aiohttp
from fastapi import Depends
from starlette.requests import Request

from api.src.config.core import settings

s3_session = aioboto3.Session(
    aws_access_key_id=settings.S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
)
# s3_client = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")


async def get_s3_client(request: Request):
    yield request.state.s3_client


S3Client = Annotated[aiohttp.ClientSession, Depends(get_s3_client)]
