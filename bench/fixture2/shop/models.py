from dataclasses import dataclass, field


@dataclass
class Product:
    sku: str
    name: str
    price: float
    stock: int = 0
    category: str = "general"


@dataclass
class OrderLine:
    sku: str
    qty: int
    unit_price: float


@dataclass
class Order:
    id: int
    customer: str
    lines: list = field(default_factory=list)
    status: str = "open"  # open, paid, cancelled
    coupon: str | None = None
