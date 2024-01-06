from uuid import UUID

from fastapi.security import HTTPBearer

security = HTTPBearer()


class NotifierFacade:
    @staticmethod
    def produce(
        *,
        message
    ) -> UUID:
        ...
