from dataclasses import dataclass, field
from typing import Dict

from app.core.receipt.interactor import Item, Receipt


@dataclass
class ReceiptRepository:
    open_receipts: Dict[str, Receipt] = field(default_factory=dict[str, Receipt])
    receipt_id: int = 0

    def fetch_open_receipt(self, cashier_id: str) -> Receipt:
        return self.open_receipts[cashier_id]

    def open_receipt(self, cashier_id: str) -> Receipt:
        self.open_receipts[cashier_id] = Receipt(
            receipt_id=str(self.receipt_id), cashier_id=cashier_id, items=[]
        )
        self.receipt_id += 1
        return self.open_receipts[cashier_id]

    def close_receipt(self, cashier_id: str) -> None:
        self.open_receipts.pop(cashier_id, None)

    def add_item(self, item_id: str, cashier_id: str) -> None:
        self.open_receipts[cashier_id].items.append(Item(item_id))
