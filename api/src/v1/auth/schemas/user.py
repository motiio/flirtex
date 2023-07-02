from typing import Optional
from uuid import UUID

from pydantic import Field, computed_field

from src.v1.auth.utils import jwt
from src.v1.config.schemas import BaseSchema
from src.v1.config.settings import settings

###############################################################
#                         In Schemas                          #
###############################################################


class UserInCreateSchema(BaseSchema):
    tg_id: int = Field(alias="id")
    tg_username: Optional[str] = Field(alias="username")
    tg_first_name: Optional[str] = Field(alias="first_name")
    tg_last_name: Optional[str] = Field(None, alias="last_name")
    tg_is_premium: Optional[bool] = Field(None, alias="is_premium")
    tg_language_code: Optional[str] = Field(None, alias="language_code")


###############################################################
#                        Out Schemas                          #
###############################################################


class UserOutSchema(BaseSchema):
    id: UUID

    tg_id: int
    tg_username: str
    tg_first_name: str
    tg_last_name: str
    tg_is_premium: bool
    tg_language_code: str

    @computed_field
    @property
    def access_token(self) -> str:
        return jwt.generate_token(
            sub=str(self.id),
            expiration_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
            secret=settings.JWT_SECRET,
        )

    class Config:
        from_attributes = True
