from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.rabbitmq import rabbitmq_connection

from .routes import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_connection.connect()
    yield
    await rabbitmq_connection.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(ws_router, prefix="/v1", tags=["ws"])

