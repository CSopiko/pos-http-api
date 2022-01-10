from dataclasses import dataclass
from typing import Dict


@dataclass
class XReportRequest:
    date: str


@dataclass
class XReportResponse:
    revenue: int
    sold_item_count: Dict[str, int]
    num_closed_receipts: int


@dataclass
class XReport:
    revenue: int
    sold_item_count: Dict[str, int]
    num_closed_receipts: int
