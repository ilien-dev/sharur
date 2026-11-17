from shop.cli import main
from shop.reports import sales_summary, to_csv


def test_summary_counts_paid_orders(book):
    book.create("ana", [("A100", 2)])
    book.create("luis", [("B100", 1)])
    book.pay(1)
    assert sales_summary(book.orders.values(), book.inventory.products) == {"orders": 1, "revenue": 29.0}


def test_to_csv():
    assert to_csv(["a", "b"], [[1, 2]]) == "a,b\n1,2\n"


def test_cli_order_pay_report(data_file, capsys):
    assert main(["--data", data_file, "order", "ana", "A100:2"]) == 0
    assert main(["--data", data_file, "pay", "1"]) == 0
    capsys.readouterr()
    assert main(["--data", data_file, "report", "--low-stock", "5"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[:2] == ["paid orders: 1", "revenue: 29.00"]
    assert "F200  Tea  5" in out
