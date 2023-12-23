from src.core.schemas import BaseSchema


class UpdateTokenOutSchema(BaseSchema):
    refresh_token: str
    access_token: str
