from pydantic import Field, computed_field, field_validator

from core.schemas import BaseSchema
from auth.application.utils.jwt import check_token_signature


class UpdateTokenRequestSchema(BaseSchema):
    value: str = Field(alias="refresh_token")

    @field_validator("value")
    @classmethod
    def check_value(cls, v: str) -> str:
        valid_token_value, _ = check_token_signature(token=v)
        return valid_token_value

    @computed_field
    def user(self) -> str:
        _, data = check_token_signature(token=self.value)
        return data["sub"]
