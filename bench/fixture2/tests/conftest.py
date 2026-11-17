import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from shop import storage  # noqa: E402
from shop.inventory import Inventory  # noqa: E402
from shop.orders import OrderBook  # noqa: E402


@pytest.fixture
def data_file(tmp_path):
    target = tmp_path / "data.json"
    shutil.copy(ROOT / "data" / "seed.json", target)
    return str(target)


@pytest.fixture
def inventory(data_file):
    products, _ = storage.load(data_file)
    return Inventory(products)


@pytest.fixture
def book(inventory):
    return OrderBook(inventory)
