from dataclasses import dataclass

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
    IReceiptRepository,
    ReceiptInteractor,
)


@dataclass
class StoreCore:
    receipt_interactor: ReceiptInteractor

    def open_receipt(self, request: OpenReceiptRequest) -> OpenReceiptResponse:
        return self.receipt_interactor.open_receipt(request)

    def add_item(self, request: AddItemRequest) -> None:
        self.receipt_interactor.add_item(request)

    def fetch_current_receipt(
        self, request: FetchReceiptRequest
    ) -> FetchReceiptResponse:
        return self.receipt_interactor.fetch_open_receipt(request)

    def close_receipt(self, request: CloseReceiptRequest) -> None:
        self.receipt_interactor.close_receipt(request)

    def x_report(self, request: XReportRequest) -> XReportResponse:
        return self.receipt_interactor.x_report(request)

    @classmethod
    def create(cls, receipt_repository: IReceiptRepository) -> "StoreCore":
        return cls(
            receipt_interactor=ReceiptInteractor(receipt_repository=receipt_repository)
        )
