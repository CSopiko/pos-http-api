from dataclasses import dataclass


@dataclass
class Cashier:
    cashier_id: str


@dataclass
class OpenReceiptRequest:
    cashier_id: str


@dataclass
class CloseReceiptRequest:
    cashier_id: str


@dataclass
class OpenReceiptResponse:
    receipt_id: str
