import json


def _ints(d):
    return all(type(v) is int for v in d.values())


def test_to_cents():
    from shop.money import to_cents
    assert [to_cents("12.50"), to_cents(12.5), to_cents(8.25), to_cents("4.1")] == [1250, 1250, 825, 410]
    assert type(to_cents(12.5)) is int


def test_to_cents_float_traps():
    from shop.money import to_cents
    assert [to_cents(1.15), to_cents("99.99"), to_cents(0.29), to_cents(99.99)] == [115, 9999, 29, 9999]


def test_fmt_takes_cents():
    from shop.money import fmt
    assert [fmt(1250), fmt(5), fmt(9999)] == ["12.50", "0.05", "99.99"]


def test_load_converts_to_cents(seed):
    from shop import storage
    products, _ = storage.load(seed)
    prices = {p.sku: p.price for p in products}
    assert prices["A100"] == 1250 and prices["A200"] == 9999 and prices["F200"] == 410
    assert all(type(v) is int for v in prices.values())


def test_save_keeps_decimals(seed, tmp_path):
    from shop import storage
    products, orders = storage.load(seed)
    path = str(tmp_path / "out.json")
    storage.save(path, products, orders)
    raw = {p["sku"]: p["price"] for p in json.load(open(path, encoding="utf-8"))["products"]}
    assert raw["A100"] == 12.5 and raw["A200"] == 99.99


def test_totals_are_int_cents(book):
    from shop.models import Order, OrderLine
    from shop.pricing import order_totals
    order = Order(1, "ana", [OrderLine("A100", 2, 1250), OrderLine("F100", 1, 825)])
    totals = order_totals(order, book.inventory.products)
    assert {k: totals[k] for k in ("subtotal", "discount", "tax", "total")} == {
        "subtotal": 3325, "discount": 0, "tax": 400, "total": 3725}
    assert _ints(totals)


def test_bulk_discount_rounds_to_int(book):
    from shop.models import Order, OrderLine
    from shop.pricing import order_totals
    totals = order_totals(Order(1, "ana", [OrderLine("G300", 10, 335)]), book.inventory.products)
    assert totals["subtotal"] in (3182, 3183)
    assert _ints(totals)


def test_order_lines_in_cents(book):
    order = book.create("ana", [("A100", 2)])
    assert order.lines[0].unit_price == 1250
    assert book.total(order.id)["total"] == 2900


def test_summary_in_cents(book):
    from shop.reports import sales_summary
    book.create("ana", [("A100", 2)])
    book.pay(1)
    assert sales_summary(book.orders.values(), book.inventory.products) == {"orders": 1, "revenue": 2900}


def test_cli_list_unchanged(seed, capsys):
    from shop.cli import main
    assert main(["--data", seed, "list"]) == 0
    assert "A100  Widget  12.50  stock=40" in capsys.readouterr().out.splitlines()


def test_cli_order_and_report_unchanged(seed, capsys):
    from shop.cli import main
    assert main(["--data", seed, "order", "ana", "A100:2"]) == 0
    assert capsys.readouterr().out.strip() == "order 1: subtotal 25.00 discount 0.00 tax 4.00 total 29.00"
    assert main(["--data", seed, "pay", "1"]) == 0
    capsys.readouterr()
    assert main(["--data", seed, "report"]) == 0
    assert capsys.readouterr().out.splitlines()[:2] == ["paid orders: 1", "revenue: 29.00"]


def test_data_file_keeps_decimal_unit_prices(seed):
    from shop.cli import main
    assert main(["--data", seed, "order", "ana", "A100:2"]) == 0
    raw = json.load(open(seed, encoding="utf-8"))
    assert raw["orders"][0]["lines"][0]["unit_price"] == 12.5
    assert raw["products"][0]["price"] == 12.5
