import json

import pytest


def _paid(book, items=(("A100", 4),)):
    order = book.create("ana", list(items))
    book.pay(order.id)
    return order


def test_return_restocks(book):
    order = _paid(book)
    book.return_items(order.id, [("A100", 1)])
    assert book.inventory.get("A100").stock == 37


def test_returns_recorded(book):
    order = _paid(book)
    book.return_items(order.id, [("A100", 1)])
    assert [(r.sku, r.qty) for r in book.get(order.id).returns] == [("A100", 1)]


def test_new_order_has_no_returns(book):
    assert list(book.create("ana", [("A100", 1)]).returns) == []


def test_open_order_rejected(book):
    from shop.orders import OrderError
    order = book.create("ana", [("A100", 4)])
    with pytest.raises(OrderError):
        book.return_items(order.id, [("A100", 1)])


def test_too_many_rejected(book):
    from shop.orders import OrderError
    order = _paid(book)
    with pytest.raises(OrderError):
        book.return_items(order.id, [("A100", 5)])
    assert book.inventory.get("A100").stock == 36


def test_cumulative_limit(book):
    from shop.orders import OrderError
    order = _paid(book)
    book.return_items(order.id, [("A100", 3)])
    with pytest.raises(OrderError):
        book.return_items(order.id, [("A100", 2)])
    assert book.inventory.get("A100").stock == 39


def test_refunded_in_totals(book):
    from shop.pricing import order_totals
    order = _paid(book)
    assert order_totals(order, book.inventory.products)["refunded"] == 0
    book.return_items(order.id, [("A100", 1)])
    assert order_totals(book.get(order.id), book.inventory.products)["refunded"] == 12.5


def test_summary_subtracts_refunds(book):
    from shop.reports import sales_summary
    order = _paid(book)
    book.return_items(order.id, [("A100", 1)])
    assert sales_summary(book.orders.values(), book.inventory.products) == {"orders": 1, "revenue": 45.5}


def test_storage_roundtrip(book, tmp_path):
    from shop import storage
    order = _paid(book)
    book.return_items(order.id, [("A100", 2)])
    path = str(tmp_path / "out.json")
    storage.save(path, list(book.inventory.products.values()), list(book.orders.values()))
    _, orders = storage.load(path)
    assert [(r.sku, r.qty) for r in orders[0].returns] == [("A100", 2)]


def test_old_file_still_loads(seed):
    from shop import storage
    raw = json.loads(open(seed, encoding="utf-8").read())
    raw["orders"] = [{"id": 1, "customer": "ana", "status": "paid", "coupon": None,
                      "lines": [{"sku": "A100", "qty": 1, "unit_price": 12.5}]}]
    open(seed, "w", encoding="utf-8").write(json.dumps(raw))
    _, orders = storage.load(seed)
    assert list(orders[0].returns) == []


def test_cli_return(seed):
    from shop import storage
    from shop.cli import main
    assert main(["--data", seed, "order", "ana", "A100:4"]) == 0
    assert main(["--data", seed, "pay", "1"]) == 0
    assert main(["--data", seed, "return", "1", "A100:1"]) == 0
    products, orders = storage.load(seed)
    assert {p.sku: p.stock for p in products}["A100"] == 37
    assert [(r.sku, r.qty) for r in orders[0].returns] == [("A100", 1)]


def test_cli_return_on_open_order_fails(seed):
    from shop.cli import main
    assert main(["--data", seed, "order", "ana", "A100:4"]) == 0
    assert main(["--data", seed, "return", "1", "A100:1"]) == 1
