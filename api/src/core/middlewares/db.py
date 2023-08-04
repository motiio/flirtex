from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

from fastapi import Request
from sqlalchemy.ext.asyncio import async_scoped_session
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


class DatabaseMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        session_factory,
    ):
        super().__init__(app)
        self.session_factory = session_factory

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid1())
        ctx_token = _request_id_ctx_var.set(request_id)
        try:
            db_session = async_scoped_session(self.session_factory, scopefunc=get_request_id)
            request.state.db = db_session()
            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            await request.state.db.close()
            _request_id_ctx_var.reset(ctx_token)
        return response
