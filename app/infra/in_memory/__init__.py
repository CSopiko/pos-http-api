from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.core.manager import XReport
from app.core.receipt.interactor import Item, Receipt


@dataclass
class ReceiptRepository:
    open_receipts: Dict[str, Receipt] = field(default_factory=dict[str, Receipt])
    closed_receipts: List[Optional[Receipt]] = field(
        default_factory=list[Optional[Receipt]]
    )
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
        self.closed_receipts.append(self.open_receipts.pop(cashier_id, None))

    def add_item(self, item_id: str, cashier_id: str) -> None:
        self.open_receipts[cashier_id].items.append(Item(item_id))

    def x_report(self, date: str) -> XReport:
        revenue: int = 0
        sold_item_count: Dict[str, int] = {}
        num_closed_receipts: int = 0
        for r in self.closed_receipts:
            if r is not None:
                num_closed_receipts += 1
                for i in r.items:
                    revenue += i.item_price
                    sold_item_count[i.item_id] = (
                        1
                        if i.item_id not in sold_item_count
                        else sold_item_count[i.item_id] + 1
                    )
        x_resp = XReport(
            revenue=revenue,
            sold_item_count=sold_item_count,
            num_closed_receipts=num_closed_receipts,
        )
        return x_resp
