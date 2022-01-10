from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core import StoreCore
from app.core.cashier.interactor import (
    CloseReceiptRequest,
    OpenReceiptRequest,
    OpenReceiptResponse,
)
from app.core.manager import XReportRequest, XReportResponse
from app.core.receipt.interactor import (
    AddItemRequest,
    FetchReceiptRequest,
    FetchReceiptResponse,
)

receipt_api = APIRouter()


def get_core(request: Request) -> StoreCore:
    core: StoreCore = request.app.state.core
    return core


@receipt_api.post("/open_receipt/{cashier_id}")
def open_receipt(
    cashier_id: str, core: StoreCore = Depends(get_core)
) -> OpenReceiptResponse:
    return core.open_receipt(OpenReceiptRequest(cashier_id=cashier_id))


@receipt_api.post("/add_item/{cashier_id, item_id}")
def add_item(
    cashier_id: str, item_id: str, core: StoreCore = Depends(get_core)
) -> None:
    core.add_item(AddItemRequest(item_id=item_id, cashier_id=cashier_id))


@receipt_api.get("/current_receipts/{cashier_id}")
def fetch_current_receipt(
    cashier_id: str, core: StoreCore = Depends(get_core)
) -> FetchReceiptResponse:
    return core.fetch_current_receipt(FetchReceiptRequest(cashier_id))


@receipt_api.post("/close_receipt/{cashier_id}")
def close_receipt(
    cashier_id: str,
    core: StoreCore = Depends(get_core),
) -> None:
    core.close_receipt(CloseReceiptRequest(cashier_id=cashier_id))


@receipt_api.get("/x_report/{date}")
def x_report(date: str, core: StoreCore = Depends(get_core)) -> XReportResponse:
    x_rep = core.x_report(XReportRequest(date=date))
    print(x_rep.revenue)
    return x_rep
