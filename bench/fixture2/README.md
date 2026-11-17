# shop

A small order book over a JSON data file.

    python -m shop.cli list
    python -m shop.cli order ana A100:2 F100:1 --coupon WELCOME10
    python -m shop.cli pay 1
    python -m shop.cli cancel 2
    python -m shop.cli report --low-stock 5

Rules:

- Bulk discount per line: 5% from 10 units, 10% from 50 units.
- A coupon takes a percentage off the subtotal. Unknown coupons are rejected.
- Tax depends on the product category and is charged on what is left after the coupon.
- Creating an order reserves stock, and an order may take the last unit. Cancelling gives the stock back. Paid orders cannot be cancelled.
- Amounts are rounded half up to two decimals.

Tests: `python -m pytest -q`
