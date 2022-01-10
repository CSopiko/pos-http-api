from dataclasses import dataclass
from typing import List, Protocol

from app.core.cashier.interactor import (
    CloseReceiptRequest,
    OpenReceiptRequest,
    OpenReceiptResponse,
)
from app.core.manager import XReport, XReportRequest, XReportResponse


@dataclass
class Item:
    item_id: str
    item_name: str = "Name"
    item_price: int = 1


@dataclass
class AddItemRequest:
    item_id: str
    cashier_id: str


@dataclass
class Receipt:
    cashier_id: str
    items: List[Item]
    receipt_id: str = "0"

    def how_much(self) -> int:
        count = 0
        for i in self.items:
            count += i.item_price
        return count


@dataclass
class FetchReceiptRequest:
    cashier_id: str


@dataclass
class FetchReceiptResponse:
    receipt_id: str
    items: List[Item]
    total: float


class IReceiptRepository(Protocol):
    def fetch_open_receipt(self, cashier_id: str) -> Receipt:
        pass

    def open_receipt(self, cashier_id: str) -> Receipt:
        pass

    def close_receipt(self, cashier_id: str) -> None:
        pass

    def add_item(self, item_id: str, cashier_id: str) -> None:
        pass

    def x_report(self, date: str) -> XReport:
        pass


@dataclass
class ReceiptInteractor:
    receipt_repository: IReceiptRepository

    def fetch_open_receipt(self, request: FetchReceiptRequest) -> FetchReceiptResponse:
        receipt = self.receipt_repository.fetch_open_receipt(
            cashier_id=request.cashier_id
        )
        return FetchReceiptResponse(
            receipt_id=receipt.receipt_id, items=receipt.items, total=receipt.how_much()
        )

    def open_receipt(self, request: OpenReceiptRequest) -> OpenReceiptResponse:
        receipt = self.receipt_repository.open_receipt(request.cashier_id)
        return OpenReceiptResponse(receipt.receipt_id)

    def close_receipt(self, request: CloseReceiptRequest) -> None:
        self.receipt_repository.close_receipt(request.cashier_id)

    def add_item(self, request: AddItemRequest) -> None:
        self.receipt_repository.add_item(request.item_id, request.cashier_id)

    def x_report(self, request: XReportRequest) -> XReportResponse:
        x_resp = self.receipt_repository.x_report(date=request.date)
        return XReportResponse(
            revenue=x_resp.revenue,
            sold_item_count=x_resp.sold_item_count,
            num_closed_receipts=x_resp.num_closed_receipts,
        )
