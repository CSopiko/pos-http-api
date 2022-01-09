from fastapi import FastAPI

from app.infra.api import receipt_api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(receipt_api)
    return app
