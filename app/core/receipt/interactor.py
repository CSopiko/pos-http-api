from dataclasses import dataclass
from typing import Dict, List, Protocol

from app.core.cashier.interactor import (
    CloseReceiptRequest,
    OpenReceiptRequest,
    OpenReceiptResponse,
)


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
    receipt_id: str
    cashier_id: str
    items: List[Item]

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


class IReceiptRepository(Protocol):
    open_receipts: Dict[str, Receipt]
    receipt_id: int

    def fetch_open_receipt(self, cashier_id: str) -> Receipt:
        pass

    def open_receipt(self, cashier_id: str) -> Receipt:
        pass

    def close_receipt(self, cashier_id: str) -> None:
        pass

    def add_item(self, item_id: str, cashier_id: str) -> None:
        pass


@dataclass
class ReceiptInteractor:
    receipt_repository: IReceiptRepository

    def fetch_open_receipt(self, request: FetchReceiptRequest) -> FetchReceiptResponse:
        receipt = self.receipt_repository.fetch_open_receipt(
            cashier_id=request.cashier_id
        )
        return FetchReceiptResponse(receipt_id=receipt.receipt_id, items=receipt.items)

    def open_receipt(self, request: OpenReceiptRequest) -> OpenReceiptResponse:
        receipt = self.receipt_repository.open_receipt(request.cashier_id)
        return OpenReceiptResponse(receipt.receipt_id)

    def close_receipt(self, request: CloseReceiptRequest) -> None:
        self.receipt_repository.close_receipt(request.cashier_id)

    def add_item(self, request: AddItemRequest) -> None:
        self.receipt_repository.add_item(request.item_id, request.cashier_id)
