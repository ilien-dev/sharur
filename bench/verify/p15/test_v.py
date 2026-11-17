import json


def _paid_order(seed):
    from shop.cli import main
    assert main(["--data", seed, "order", "ana", "A100:2"]) == 0
    assert main(["--data", seed, "pay", "1"]) == 0
    return main


def test_report_json(seed, capsys):
    main = _paid_order(seed)
    capsys.readouterr()
    assert main(["--data", seed, "report", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == {"orders": 1, "revenue": 29.0}


def test_report_json_empty(seed, capsys):
    from shop.cli import main
    assert main(["--data", seed, "report", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == {"orders": 0, "revenue": 0}


def test_plain_report_unchanged(seed, capsys):
    main = _paid_order(seed)
    capsys.readouterr()
    assert main(["--data", seed, "report"]) == 0
    assert capsys.readouterr().out.splitlines()[:2] == ["paid orders: 1", "revenue: 29.00"]
