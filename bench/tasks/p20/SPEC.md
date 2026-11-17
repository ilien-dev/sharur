# Work to do

1. The test suite fails. Fix the code; the tests and the README rules are right.
2. Order ids: `OrderBook.next_id()` returns the highest existing id plus one, or 1 when there are no orders.
3. `OrderBook.create` is all or nothing: if any item cannot be reserved, no stock changes and no order is created.
4. Cancelling an order that is already cancelled raises `OrderError`.
5. Coupons get a minimum subtotal. `pricing.COUPONS` maps each code to `{"rate": float, "min_subtotal": float}`: WELCOME10 is 10% with no minimum, VIP20 is 20% from a subtotal of 100. Below the minimum the coupon is accepted and the discount is 0. Unknown codes are still rejected with `ValueError`.
6. Stock audit log: `Inventory.log` is a list of `(sku, delta, reason)` tuples. `reserve` appends `(sku, -qty, "reserve")` and `release` appends `(sku, qty, "release")`. A call that fails logs nothing.
7. `reports.sales_by_category` counts paid orders only.
8. `reports.top_customers(orders, products, n=3)` returns `[(customer, revenue), ...]` over paid orders. Revenue is the sum of the customer's order totals, rounded to two decimals. Sorted by revenue, highest first, then by customer name, cut to `n` entries.
9. CLI `report --by-category` prints, after the usual two lines, one line per category as `<category>  <amount>` (two spaces, two decimals), categories in alphabetical order.
10. CLI `import-products FILE` reads a CSV with the header `sku,name,price,stock,category`. Existing SKUs are updated and new ones are added. A row whose price or stock is not a number, or is negative, is skipped. It prints `imported N, skipped M`. The work is done by `storage.import_products(csv_path, products)`, where `products` is the dict of SKU to Product; it changes that dict and returns `(imported, skipped)`.
11. Add tests for all of the above and update the README.
