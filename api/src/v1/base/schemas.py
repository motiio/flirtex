from datetime import datetime
from typing import Any, Callable
from zoneinfo import ZoneInfo

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class BaseSchema(BaseModel):
    class Config:
        populate_by_field_name = True


class BaseS3Schema(BaseModel):
    key: str
