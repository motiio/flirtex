from fastapi import FastAPI

from .routes import ws_router

app = FastAPI()
app.include_router(ws_router, prefix="/v1", tags=["ws"])
