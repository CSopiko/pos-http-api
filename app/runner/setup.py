from fastapi import FastAPI

from app.core import StoreCore
from app.core.receipt.interactor import IReceiptRepository
from app.infra.api import receipt_api
from app.infra.in_memory import ReceiptRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(receipt_api)
    app.state.core = StoreCore.create(receipt_repository=setup_receipt_repository())
    return app


def setup_receipt_repository() -> IReceiptRepository:
    repository = ReceiptRepository()
    return repository
