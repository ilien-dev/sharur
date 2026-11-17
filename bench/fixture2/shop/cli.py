import argparse
import sys

from . import storage
from .inventory import Inventory, OutOfStock
from .money import fmt
from .orders import OrderBook, OrderError
from .reports import low_stock_lines, sales_summary


def parse_item(text):
    sku, _, qty = text.partition(":")
    return sku, int(qty or 1)


def build_parser():
    parser = argparse.ArgumentParser(prog="shop")
    parser.add_argument("--data", default="data/seed.json")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    order = sub.add_parser("order")
    order.add_argument("customer")
    order.add_argument("items", nargs="+", help="SKU:QTY")
    order.add_argument("--coupon")
    for name in ("pay", "cancel"):
        cmd = sub.add_parser(name)
        cmd.add_argument("id", type=int)
    report = sub.add_parser("report")
    report.add_argument("--low-stock", type=int, default=None)
    return parser


def run(args, inventory, book):
    if args.cmd == "list":
        for p in sorted(inventory.products.values(), key=lambda p: p.sku):
            print(f"{p.sku}  {p.name}  {fmt(p.price)}  stock={p.stock}")
    elif args.cmd == "order":
        order = book.create(args.customer, [parse_item(i) for i in args.items], coupon=args.coupon)
        t = book.total(order.id)
        print(f"order {order.id}: subtotal {fmt(t['subtotal'])} discount {fmt(t['discount'])} "
              f"tax {fmt(t['tax'])} total {fmt(t['total'])}")
    elif args.cmd == "pay":
        book.pay(args.id)
        print(f"order {args.id} paid")
    elif args.cmd == "cancel":
        book.cancel(args.id)
        print(f"order {args.id} cancelled")
    elif args.cmd == "report":
        summary = sales_summary(book.orders.values(), inventory.products)
        print(f"paid orders: {summary['orders']}")
        print(f"revenue: {fmt(summary['revenue'])}")
        if args.low_stock is not None:
            for line in low_stock_lines(inventory, args.low_stock):
                print(line)


def main(argv=None):
    args = build_parser().parse_args(argv)
    products, orders = storage.load(args.data)
    inventory = Inventory(products)
    book = OrderBook(inventory, orders)
    try:
        run(args, inventory, book)
    except (OrderError, OutOfStock, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    storage.save(args.data, list(inventory.products.values()), list(book.orders.values()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
