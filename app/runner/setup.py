from fastapi import FastAPI

from app.core import StoreCore
from app.core.receipt.interactor import IReceiptRepository
from app.infra.api import receipt_api
from app.infra.database.sqlit_db import SqlitReceiptRepository
from app.infra.in_memory import ReceiptRepository


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(receipt_api)
    app.state.core = StoreCore.create(
        receipt_repository=setup_receipt_repository_sqlite()
    )
    return app


def setup_receipt_repository() -> IReceiptRepository:
    repository = ReceiptRepository()
    return repository


def setup_receipt_repository_sqlite() -> IReceiptRepository:
    repository = SqlitReceiptRepository()

    repository.add_item_to_store("0", "Apple", 1)
    repository.add_item_to_store("1", "DampaliApple", 0.5)
    repository.add_item_to_store("2", "Milk", 3)
    repository.add_item_to_store("3", "Child", 5)

    return repository
