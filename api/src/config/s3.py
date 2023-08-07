from typing import Annotated

import aioboto3
from fastapi import Depends
from starlette.requests import Request

from src.config.settings import settings


def create_s3_session():
    return aioboto3.Session(
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    )


def get_s3(request: Request):
    return request.state.s3


S3Session = Annotated[aioboto3.Session, Depends(get_s3)]
