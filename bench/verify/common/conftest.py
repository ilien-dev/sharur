import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SEED = {
    "products": [
        {"sku": "A100", "name": "Widget", "price": 12.5, "stock": 40, "category": "general"},
        {"sku": "A200", "name": "Gadget", "price": 99.99, "stock": 3, "category": "general"},
        {"sku": "B100", "name": "Novel", "price": 15.0, "stock": 100, "category": "books"},
        {"sku": "F100", "name": "Coffee", "price": 8.25, "stock": 60, "category": "food"},
        {"sku": "F200", "name": "Tea", "price": 4.1, "stock": 5, "category": "food"},
        {"sku": "G300", "name": "Cable", "price": 3.35, "stock": 500, "category": "general"},
    ],
    "orders": [],
}


@pytest.fixture
def seed(tmp_path):
    target = tmp_path / "data.json"
    target.write_text(json.dumps(SEED), encoding="utf-8")
    return str(target)


@pytest.fixture
def book(seed):
    from shop import storage
    from shop.inventory import Inventory
    from shop.orders import OrderBook
    products, orders = storage.load(seed)
    return OrderBook(Inventory(products), orders)
