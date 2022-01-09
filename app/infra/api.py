from fastapi import APIRouter

receipt_api = APIRouter()


@receipt_api.get("/receipts")
def fetch_receipts() -> None:
    pass
