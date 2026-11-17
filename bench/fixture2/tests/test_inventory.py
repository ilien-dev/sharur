import pytest

from shop.inventory import OutOfStock


def test_reserve_reduces_stock(inventory):
    inventory.reserve("A100", 4)
    assert inventory.get("A100").stock == 36


def test_reserve_last_units(inventory):
    inventory.reserve("A200", 3)
    assert inventory.get("A200").stock == 0


def test_out_of_stock(inventory):
    with pytest.raises(OutOfStock):
        inventory.reserve("A200", 4)


def test_low_stock(inventory):
    assert [p.sku for p in inventory.low_stock(5)] == ["A200", "F200"]
