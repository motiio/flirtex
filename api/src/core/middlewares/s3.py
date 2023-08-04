class S3Middleware(
    BaseHTTPMiddleware,
):
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


@api.middleware("http")
async def s3_resource_middleware(request: Request, call_next):
    request.state.s3 = create_s3_session()
    response = await call_next(request)
    return response
