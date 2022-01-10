from app.core.cashier.interactor import (
    Cashier,
    CloseReceiptRequest,
    OpenReceiptRequest,
    OpenReceiptResponse,
)
from app.core.receipt.interactor import (
    AddItemRequest,
    FetchReceiptRequest,
    FetchReceiptResponse,
    Item,
    Receipt,
)


def test_item_empty() -> None:
    empty_item = Item(item_id="", item_name="", item_price=0)
    assert empty_item.item_id == ""
    assert empty_item.item_name == ""
    assert empty_item.item_price == 0


def test_item_basic() -> None:
    empty_item = Item(item_id="0", item_name="Basic", item_price=1)
    assert empty_item.item_id == "0"
    assert empty_item.item_name == "Basic"
    assert empty_item.item_price == 1


def test_receipt_empty() -> None:
    empty_receipt = Receipt(receipt_id="", cashier_id="", items=[])
    assert empty_receipt.receipt_id == ""
    assert empty_receipt.cashier_id == ""
    assert len(empty_receipt.items) == 0


def test_receipt_basic() -> None:
    basic_receipt = Receipt(receipt_id="1", cashier_id="1", items=[])
    assert basic_receipt.receipt_id == "1"
    assert basic_receipt.cashier_id == "1"
    assert len(basic_receipt.items) == 0


def test_receipt_basic_amount() -> None:
    basic_receipt = Receipt(
        receipt_id="1",
        cashier_id="1",
        items=[
            Item(item_id="1", item_name="Apple", item_price=1),
        ],
    )

    assert basic_receipt.how_much() == 1


def test_receipt_amount() -> None:
    basic_receipt = Receipt(
        receipt_id="1",
        cashier_id="1",
        items=[
            Item(item_id="1", item_name="Apple", item_price=1),
            Item(item_id="2", item_name="Milk", item_price=2),
        ],
    )

    assert basic_receipt.how_much() == 3


def test_add_item_request_empty() -> None:
    empty_request = AddItemRequest(item_id="", cashier_id="")
    assert empty_request.item_id == ""
    assert empty_request.cashier_id == ""


def test_add_item_request_basic() -> None:
    basic_request = AddItemRequest(item_id="0", cashier_id="0")
    assert basic_request.item_id == "0"
    assert basic_request.cashier_id == "0"


def test_fetch_receipt_request_empty() -> None:
    empty_request = FetchReceiptRequest(cashier_id="")
    assert empty_request.cashier_id == ""


def test_fetch_receipt_request_basic() -> None:
    basic_request = FetchReceiptRequest(cashier_id="0")
    assert basic_request.cashier_id == "0"


def test_fetch_receipt_response_empty() -> None:
    empty_response = FetchReceiptResponse(receipt_id="", items=[])
    assert empty_response.receipt_id == ""
    assert len(empty_response.items) == 0


def test_fetch_receipt_response_basic() -> None:
    basic_response = FetchReceiptResponse(
        receipt_id="0",
        items=[
            Item(item_id="1", item_name="Apple", item_price=1),
        ],
    )
    assert basic_response.receipt_id == "0"
    assert len(basic_response.items) == 1


def test_cashier_empty() -> None:
    assert Cashier(cashier_id="").cashier_id == ""


def test_cashier_basic() -> None:
    assert Cashier(cashier_id="1").cashier_id == "1"


def test_open_receipt_request_empty() -> None:
    assert OpenReceiptRequest(cashier_id="").cashier_id == ""


def test_open_receipt_request_basic() -> None:
    assert OpenReceiptRequest(cashier_id="1").cashier_id == "1"


def test_close_receipt_request_empty() -> None:
    assert CloseReceiptRequest(cashier_id="").cashier_id == ""


def test_close_receipt_request_basic() -> None:
    assert CloseReceiptRequest(cashier_id="1").cashier_id == "1"


def test_open_receipt_response_empty() -> None:
    assert OpenReceiptResponse(receipt_id="").receipt_id == ""


def test_open_receipt_response_basic() -> None:
    assert OpenReceiptResponse(receipt_id="1").receipt_id == "1"
