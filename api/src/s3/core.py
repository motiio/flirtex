import aioboto3

from src.config.core import settings

s3_session = aioboto3.Session(
    aws_access_key_id=settings.S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
)
