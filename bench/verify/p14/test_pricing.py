import pytest

from shop.models import Order, OrderLine
from shop.pricing import bulk_discount, coupon_rate, line_total, order_totals


def test_no_bulk_discount_below_ten():
    assert bulk_discount(9) == 0.0


def test_bulk_discount_from_ten():
    assert bulk_discount(10) == 0.05


def test_bulk_discount_from_fifty():
    assert bulk_discount(50) == 0.10


def test_line_total():
    assert line_total(OrderLine("A100", 2, 12.5)) == 25.0


def test_unknown_coupon():
    with pytest.raises(ValueError):
        coupon_rate("NOPE")


def test_totals_without_coupon(inventory):
    order = Order(1, "ana", [OrderLine("A100", 2, 12.5), OrderLine("F100", 1, 8.25)])
    assert order_totals(order, inventory.products) == {
        "subtotal": 33.25, "discount": 0.0, "tax": 4.0, "total": 37.25}


def test_tax_is_charged_after_coupon(inventory):
    order = Order(1, "ana", [OrderLine("A100", 2, 12.5)], coupon="WELCOME10")
    assert order_totals(order, inventory.products) == {
        "subtotal": 25.0, "discount": 2.5, "tax": 3.6, "total": 26.1}
