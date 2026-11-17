from .money import round_money

TAX_RATES = {"general": 0.16, "food": 0.0, "books": 0.0}
COUPONS = {"WELCOME10": 0.10, "VIP20": 0.20}


def bulk_discount(qty):
    """5% from 10 units, 10% from 50 units."""
    if qty >= 10:
        return 0.05
    if qty >= 50:
        return 0.10
    return 0.0


def line_total(line):
    return line.qty * line.unit_price * (1 - bulk_discount(line.qty))


def coupon_rate(code):
    if code is None:
        return 0.0
    if code not in COUPONS:
        raise ValueError(f"unknown coupon: {code}")
    return COUPONS[code]


def order_totals(order, products):
    """Return subtotal, discount, tax and total for an order.

    subtotal: sum of the line totals, bulk discount already applied
    discount: coupon discount, taken from the subtotal
    tax: per product category, on what is left of each line after the coupon
    total: subtotal - discount + tax
    """
    rate = coupon_rate(order.coupon)
    subtotal = 0.0
    tax = 0.0
    for line in order.lines:
        amount = line_total(line)
        subtotal += amount
        category = products[line.sku].category
        tax += amount * TAX_RATES.get(category, TAX_RATES["general"])
    discount = subtotal * rate
    total = subtotal - discount + tax
    return {
        "subtotal": round_money(subtotal),
        "discount": round_money(discount),
        "tax": round_money(tax),
        "total": round_money(total),
    }
