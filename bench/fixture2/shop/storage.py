import json
from dataclasses import asdict

from .models import Order, OrderLine, Product


def load(path):
    """Return (products, orders) from a JSON data file."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    products = [Product(**p) for p in raw.get("products", [])]
    orders = []
    for o in raw.get("orders", []):
        lines = [OrderLine(**line) for line in o.get("lines", [])]
        orders.append(Order(o["id"], o["customer"], lines, o.get("status", "open"), o.get("coupon")))
    return products, orders


def save(path, products, orders):
    raw = {"products": [asdict(p) for p in products], "orders": [asdict(o) for o in orders]}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(raw, fh, indent=1)
