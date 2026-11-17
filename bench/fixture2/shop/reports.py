import csv
import io

from .money import round_money
from .pricing import line_total, order_totals


def sales_summary(orders, products):
    paid = [o for o in orders if o.status == "paid"]
    revenue = sum(order_totals(o, products)["total"] for o in paid)
    return {"orders": len(paid), "revenue": round_money(revenue)}


def sales_by_category(orders, products):
    """Revenue before coupons and tax, per product category."""
    out = {}
    for order in orders:
        for line in order.lines:
            category = products[line.sku].category
            out[category] = out.get(category, 0.0) + line_total(line)
    return {k: round_money(v) for k, v in sorted(out.items())}


def low_stock_lines(inventory, threshold=5):
    return [f"{p.sku}  {p.name}  {p.stock}" for p in inventory.low_stock(threshold)]


def to_csv(headers, rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return buf.getvalue()
