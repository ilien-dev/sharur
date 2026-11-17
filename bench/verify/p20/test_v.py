import pytest


def _order(lines, coupon=None):
    from shop.models import Order, OrderLine
    return Order(1, "ana", [OrderLine(*line) for line in lines], coupon=coupon)


# 1
def test_bulk_discount_fifty():
    from shop.pricing import bulk_discount
    assert bulk_discount(50) == 0.10 and bulk_discount(10) == 0.05


def test_reserve_last_units(book):
    book.inventory.reserve("A200", 3)
    assert book.inventory.get("A200").stock == 0


def test_tax_after_coupon(book):
    from shop.pricing import order_totals
    totals = order_totals(_order([("A100", 2, 12.5)], "WELCOME10"), book.inventory.products)
    assert (totals["subtotal"], totals["discount"], totals["tax"], totals["total"]) == (25.0, 2.5, 3.6, 26.1)


# 2
def test_next_id(book):
    from shop.models import Order
    from shop.orders import OrderBook
    assert book.next_id() == 1
    assert OrderBook(book.inventory, [Order(5, "x"), Order(2, "y")]).next_id() == 6


# 3
def test_create_is_atomic(book):
    from shop.inventory import OutOfStock
    with pytest.raises(OutOfStock):
        book.create("ana", [("A100", 2), ("A200", 99)])
    assert book.inventory.get("A100").stock == 40
    assert len(book.orders) == 0


# 4
def test_cancel_twice(book):
    from shop.orders import OrderError
    book.create("ana", [("A100", 2)])
    book.cancel(1)
    with pytest.raises(OrderError):
        book.cancel(1)
    assert book.inventory.get("A100").stock == 40


# 5
def test_coupon_table():
    from shop.pricing import COUPONS
    assert COUPONS["VIP20"]["rate"] == pytest.approx(0.2) and COUPONS["VIP20"]["min_subtotal"] == 100
    assert COUPONS["WELCOME10"]["rate"] == pytest.approx(0.1) and COUPONS["WELCOME10"]["min_subtotal"] == 0


def test_coupon_below_minimum(book):
    from shop.pricing import order_totals
    totals = order_totals(_order([("A100", 2, 12.5)], "VIP20"), book.inventory.products)
    assert (totals["discount"], totals["total"]) == (0, 29.0)


def test_coupon_above_minimum(book):
    from shop.pricing import order_totals
    totals = order_totals(_order([("A100", 10, 12.5)], "VIP20"), book.inventory.products)
    assert (totals["subtotal"], totals["discount"], totals["tax"], totals["total"]) == (118.75, 23.75, 15.2, 110.2)


def test_unknown_coupon_rejected(book):
    with pytest.raises(ValueError):
        book.create("ana", [("A100", 1)], coupon="NOPE")


# 6
def test_audit_log(book):
    from shop.inventory import OutOfStock
    inv = book.inventory
    assert list(inv.log) == []
    inv.reserve("A100", 2)
    inv.release("A100", 1)
    with pytest.raises(OutOfStock):
        inv.reserve("A200", 99)
    assert [tuple(e) for e in inv.log] == [("A100", -2, "reserve"), ("A100", 1, "release")]


# 7
def test_by_category_paid_only(book):
    from shop.reports import sales_by_category
    book.create("ana", [("A100", 2)])
    book.create("luis", [("B100", 1)])
    book.pay(1)
    assert sales_by_category(book.orders.values(), book.inventory.products) == {"general": 25.0}


# 8
def _customers(book):
    for customer, items in [("bob", [("A100", 2)]), ("ana", [("A100", 2)]), ("ana", [("B100", 1)]),
                            ("luis", [("A200", 1)]), ("zoe", [("A100", 30)])]:
        book.create(customer, items)
    for order_id in (1, 2, 3, 4):
        book.pay(order_id)


def test_top_customers(book):
    from shop.reports import top_customers
    _customers(book)
    assert [tuple(r) for r in top_customers(book.orders.values(), book.inventory.products)] == [
        ("luis", 115.99), ("ana", 44.0), ("bob", 29.0)]


def test_top_customers_n_and_ties(book):
    from shop.reports import top_customers
    book.create("bob", [("A100", 2)])
    book.create("ana", [("A100", 2)])
    book.pay(1)
    book.pay(2)
    products = book.inventory.products
    assert [tuple(r) for r in top_customers(book.orders.values(), products)] == [("ana", 29.0), ("bob", 29.0)]
    assert [tuple(r) for r in top_customers(book.orders.values(), products, n=1)] == [("ana", 29.0)]


# 9
def test_cli_by_category(seed, capsys):
    from shop.cli import main
    assert main(["--data", seed, "order", "ana", "A100:2", "F100:1"]) == 0
    assert main(["--data", seed, "order", "luis", "B100:1"]) == 0
    assert main(["--data", seed, "pay", "1"]) == 0
    capsys.readouterr()
    assert main(["--data", seed, "report", "--by-category"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[:2] == ["paid orders: 1", "revenue: 37.25"]
    assert out[2:4] == ["food  8.25", "general  25.00"]


# 10
CSV = "sku,name,price,stock,category\nA100,Widget,13.0,50,general\nN1,New,1.5,7,food\nX1,Bad,abc,1,food\nX2,Neg,1.0,-3,food\n"


def test_import_products(book, tmp_path):
    from shop import storage
    path = tmp_path / "in.csv"
    path.write_text(CSV, encoding="utf-8")
    products = book.inventory.products
    assert tuple(storage.import_products(str(path), products)) == (2, 2)
    assert (products["A100"].price, products["A100"].stock) == (13.0, 50)
    assert (products["N1"].name, products["N1"].price, products["N1"].stock, products["N1"].category) == ("New", 1.5, 7, "food")
    assert "X1" not in products and "X2" not in products


def test_cli_import_products(seed, tmp_path, capsys):
    from shop import storage
    from shop.cli import main
    path = tmp_path / "in.csv"
    path.write_text(CSV, encoding="utf-8")
    assert main(["--data", seed, "import-products", str(path)]) == 0
    assert "imported 2, skipped 2" in capsys.readouterr().out
    products, _ = storage.load(seed)
    assert {p.sku: p.stock for p in products}["N1"] == 7
