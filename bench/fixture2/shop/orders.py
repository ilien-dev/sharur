from .models import Order, OrderLine
from .pricing import coupon_rate, order_totals


class OrderError(Exception):
    pass


class OrderBook:
    def __init__(self, inventory, orders=None):
        self.inventory = inventory
        self.orders = {o.id: o for o in (orders or [])}

    def next_id(self):
        return len(self.orders) + 1

    def get(self, order_id):
        if order_id not in self.orders:
            raise OrderError(f"no order {order_id}")
        return self.orders[order_id]

    def create(self, customer, items, coupon=None):
        """items: list of (sku, qty). Reserves the stock."""
        if not items:
            raise OrderError("empty order")
        coupon_rate(coupon)
        lines = []
        for sku, qty in items:
            self.inventory.reserve(sku, qty)
            lines.append(OrderLine(sku, qty, self.inventory.get(sku).price))
        order = Order(self.next_id(), customer, lines, coupon=coupon)
        self.orders[order.id] = order
        return order

    def pay(self, order_id):
        order = self.get(order_id)
        if order.status != "open":
            raise OrderError(f"order {order_id} is {order.status}")
        order.status = "paid"
        return order

    def cancel(self, order_id):
        order = self.get(order_id)
        if order.status == "paid":
            raise OrderError("paid orders cannot be cancelled")
        for line in order.lines:
            self.inventory.release(line.sku, line.qty)
        order.status = "cancelled"
        return order

    def total(self, order_id):
        return order_totals(self.get(order_id), self.inventory.products)
