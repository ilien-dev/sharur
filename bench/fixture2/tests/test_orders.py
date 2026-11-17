import pytest

from shop.orders import OrderError


def test_create_reserves_stock(book):
    order = book.create("ana", [("A100", 2), ("F100", 1)])
    assert order.id == 1
    assert book.inventory.get("A100").stock == 38
    assert [line.unit_price for line in order.lines] == [12.5, 8.25]


def test_pay(book):
    book.create("ana", [("A100", 1)])
    assert book.pay(1).status == "paid"
    with pytest.raises(OrderError):
        book.pay(1)


def test_cancel_releases_stock(book):
    book.create("ana", [("A100", 2)])
    book.cancel(1)
    assert book.inventory.get("A100").stock == 40


def test_paid_orders_cannot_be_cancelled(book):
    book.create("ana", [("A100", 1)])
    book.pay(1)
    with pytest.raises(OrderError):
        book.cancel(1)


def test_unknown_coupon_rejected(book):
    with pytest.raises(ValueError):
        book.create("ana", [("A100", 1)], coupon="NOPE")
