from typing import Annotated

import boto3
from fastapi import Depends
from starlette.requests import Request

from src.config.core import settings

s3_client = boto3.session.Session(
    aws_access_key_id=settings.S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
).client("s3", endpoint_url="https://storage.yandexcloud.net")


def get_s3(request: Request):
    return request.state.s3


S3Session = Annotated[s3_client, Depends(get_s3)]
