from uuid import UUID

from pydantic import computed_field

from src.v1.auth.utils import jwt
from src.v1.schemas import BaseSchema
from src.v1.config.settings import settings

###############################################################
#                         In Schemas                          #
###############################################################


class RefreshTokenInCreateSchema(BaseSchema):
    user: UUID
    user_agent: str

    @computed_field  # type: ignore
    @property
    def value(self) -> str:
        return jwt.generate_token(
            sub=str(self.user),
            expiration_seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
            secret=settings.JWT_SECRET,
        )


class RefreshTokenInUpdateSchema(RefreshTokenInCreateSchema):
    ...


###############################################################
#                        Out Schemas                          #
###############################################################


class RefreshTokenOutSchema(BaseSchema):
    user: UUID
    value: str
    user_agent: str

    class Config:
        from_attributes = True
