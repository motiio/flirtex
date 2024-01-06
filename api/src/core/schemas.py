from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")


class PaginationSchema(BaseSchema):
    total: int
    limit: int
    offset: int
